import boto3
from datetime import datetime, timezone

def lambda_handler(event, context):
    total_savings = 0
    total_deleted = 0

    ec2_global = boto3.client('ec2')
    regions = ec2_global.describe_regions()['Regions']

    print("Starting snapshot cleanup process...")

    for region in regions:
        region_name = region['RegionName']
        ec2 = boto3.client('ec2', region_name=region_name)

        print(f"\nChecking region: {region_name}")

        try:
            snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
        except Exception as e:
            print(f"Error fetching snapshots in {region_name}: {str(e)}")
            continue

        print(f"Snapshots found: {len(snapshots)}")

        for snapshot in snapshots:
            snapshot_id = snapshot['SnapshotId']
            volume_id = snapshot.get('VolumeId', 'N/A')

            print(f"\nProcessing Snapshot: {snapshot_id}")

            # 🔹 AGE CHECK
            age_days = (datetime.now(timezone.utc) - snapshot['StartTime']).days
            print(f"Age: {age_days} days")

            # 🔹 TAG PROTECTION
            tags = snapshot.get('Tags', [])
            protected = any(tag['Key'] == 'DoNotDelete' and tag['Value'] == 'true' for tag in tags)

            if protected:
                print("Skipped (Protected by tag)")
                continue

            # 🔹 CHECK IF VOLUME EXISTS
            volume_exists = True
            try:
                if volume_id != 'N/A':
                    ec2.describe_volumes(VolumeIds=[volume_id])
            except Exception:
                volume_exists = False

            print(f"Volume exists: {volume_exists}")

            #  DELETE CONDITION (SAFE)
            # if not volume_exists and age_days > 30:
            size = snapshot['VolumeSize']
            cost = size * 5  # ₹5 per GB (example)

            try:
                print(f"Deleting snapshot: {snapshot_id}")
                ec2.delete_snapshot(SnapshotId=snapshot_id)

                total_savings += cost
                total_deleted += 1

                print(f"Deleted snapshot: {snapshot_id}")
                print(f"Saved: ₹{cost}")

            except Exception as e:
                print(f"Error deleting {snapshot_id}: {str(e)}")
            # else:
            #     print("Skipped (Still in use or not old enough)")

    # 🔹 FINAL REPORT
    print("\n===== FINAL REPORT =====")
    print(f"Total snapshots deleted: {total_deleted}")
    print(f"Total savings: ₹{total_savings}")

    monthly_savings = total_savings * 4
    yearly_savings = monthly_savings * 12

    print(f"Estimated Monthly Savings: ₹{monthly_savings}")
    print(f"Estimated Yearly Savings: ₹{yearly_savings}")

    # 🔹 SNS NOTIFICATION
    try:
        sns = boto3.client('sns', region_name='us-east-1')  # change if needed

        sns.publish(
            TopicArn='arn:aws:sns:us-east-1:675079658906:Default_CloudWatch_Alarms_Topic', #keep your SNS Arn
            Message=(
                f"Snapshot Cleanup Report:\n"
                f"Deleted: {total_deleted}\n"
                f"Total Savings: ₹{total_savings}\n"
                f"Monthly: ₹{monthly_savings}\n"
                f"Yearly: ₹{yearly_savings}"
            ),
            Subject='AWS Cost Optimization Report'
        )

        print("SNS notification sent successfully")

    except Exception as e:
        print(f"SNS Error: {str(e)}")

    return {
        "status": "completed",
        "deleted": total_deleted,
        "savings": total_savings
    }
