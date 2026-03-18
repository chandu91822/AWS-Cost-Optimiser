# 🚀 AWS Cost Optimization System (Serverless)

## 📌 Overview

This project is a **serverless AWS cost optimization system** designed to identify and clean up unused EBS snapshots across multiple regions.

It leverages **AWS Lambda, Boto3, and SNS** to automate snapshot analysis, safe deletion, and cost reporting — helping reduce unnecessary cloud storage expenses.

---

## 🎯 Key Features

* 🔄 **Multi-Region Scanning**

  * Automatically scans all AWS regions

* 🧠 **Intelligent Filtering**

  * Skips protected snapshots using tags (`DoNotDelete=true`)
  * Checks if associated volumes still exist
  * Supports age-based filtering

* 💰 **Cost Estimation**

  * Calculates savings based on snapshot size
  * Provides total, monthly, and yearly savings

* ⚡ **Serverless Execution**

  * Runs on AWS Lambda
  * Can be triggered using EventBridge (cron scheduling)

* 📢 **Automated Notifications**

  * Sends cleanup reports via SNS (Email alerts)

* 🛡️ **Safe Deletion**

  * Prevents accidental deletion of critical resources

---

## 🏗️ Architecture

```
EventBridge (Scheduler)
        ↓
   AWS Lambda
        ↓
  EC2 Snapshots (Scan & Analyze)
        ↓
 Delete Unused Snapshots
        ↓
   SNS Notification (Report)
```

---

## 🛠️ Technologies Used

* AWS Lambda (Python)
* Boto3 (AWS SDK)
* Amazon EC2 (Snapshots & Volumes)
* Amazon SNS (Notifications)
* CloudWatch Logs (Monitoring)

---

## ⚙️ How It Works

1. Fetch all AWS regions
2. Retrieve snapshots owned by the account
3. For each snapshot:

   * Check age
   * Verify associated volume existence
   * Skip protected snapshots (via tags)
4. Delete eligible snapshots
5. Calculate cost savings
6. Send summary report via SNS

---

## 📂 Project Structure

```
.
├── lambda_function.py   # Main AWS Lambda logic
├── requirements.txt     # Dependencies (if needed)
└── README.md            # Documentation
```

---

## 🔐 IAM Permissions Required

Ensure your Lambda role has:

* ec2:DescribeSnapshots
* ec2:DeleteSnapshot
* ec2:DescribeVolumes
* ec2:DescribeRegions
* sns:Publish
* logs:CreateLogGroup
* logs:CreateLogStream
* logs:PutLogEvents

---

## 🚀 Deployment Steps

1. Create an AWS Lambda function (Python 3.x)
2. Paste the code into `lambda_function.py`
3. Attach IAM role with required permissions
4. Configure SNS topic and email subscription
5. (Optional) Create EventBridge rule for automation

---

## 🧪 Sample Output

```
Checking region: ap-south-1
Snapshots found: 5

Processing Snapshot: snap-12345
Age: 45 days
Volume exists: False
Deleting snapshot: snap-12345
Saved: ₹100

===== FINAL REPORT =====
Total snapshots deleted: 2
Total savings: ₹200
```

---

## 📈 Future Enhancements

* 🔹 Simulation Mode (preview before deletion)
* 🔹 Smart Deletion Scoring System
* 🔹 DynamoDB logging for historical analysis
* 🔹 Multi-resource optimization (EC2, EBS, AMIs)
* 🔹 CLI-based control interface

---

## 👨‍💻 Author

Developed as part of a cloud computing project focusing on **cost optimization, automation, and serverless architecture**.

---

## ⭐ Why This Project?

This project demonstrates:

* Real-world cloud cost optimization
* Serverless architecture design
* AWS service integration
* DevOps and automation mindset

---

## 📬 Contact

Feel free to connect for collaboration or suggestions!
