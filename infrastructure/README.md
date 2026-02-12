# AWS Infrastructure for AI Assistant

This directory contains AWS infrastructure scaffolding for deploying your AI assistant with secure credentials, scheduled tasks, file storage, and monitoring.

## Why AWS?

When building an AI assistant that operates autonomously, you need:

- **Secure secret storage** - API keys, tokens, and credentials stored encrypted
- **Scheduled tasks** - Run automation on a schedule (daily digests, backups)
- **File storage** - Backup your vault, store logs and artifacts
- **Monitoring** - Get alerted when something goes wrong or costs spike

AWS provides all of this with a generous free tier that covers most personal use cases.

## What's Included

This scaffold includes:

- **Secrets Manager** - Encrypted storage for API keys and credentials
- **Lambda Functions** - Serverless functions for scheduled tasks and webhooks
- **S3 Buckets** - File storage for backups and artifacts
- **CloudWatch** - Logging and monitoring
- **Budget Alerts** - Get notified before costs exceed your threshold

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Your AI Assistant                    │
│                    (runs on your machine)                │
└───────────┬─────────────────────────────────┬───────────┘
            │                                 │
            │ Read secrets                    │ Write backups
            │                                 │
            ▼                                 ▼
    ┌───────────────┐                ┌───────────────┐
    │ AWS Secrets   │                │  S3 Bucket    │
    │   Manager     │                │  (Backups)    │
    └───────────────┘                └───────────────┘
            │
            │ Retrieve API keys
            │
            ▼
    ┌───────────────────────────────────────────────┐
    │           External Services                    │
    │  (Gmail, Slack, Shopify, etc.)                │
    └───────────────────────────────────────────────┘

    ┌───────────────┐
    │ EventBridge   │ ──► Lambda (Scheduled tasks)
    └───────────────┘

    ┌───────────────┐
    │ API Gateway   │ ──► Lambda (Webhooks)
    └───────────────┘

    ┌───────────────┐
    │ CloudWatch    │ ──► SNS ──► Email Alerts
    └───────────────┘
```

## Prerequisites

Before you begin:

1. **AWS Account** - [Sign up for free](https://aws.amazon.com/free/)
2. **AWS CLI** - [Install AWS CLI](https://aws.amazon.com/cli/)
3. **AWS Credentials** - Configure credentials with `aws configure`
4. **IAM Permissions** - Your user needs permissions to create resources

## Getting Started

### 1. Bootstrap Your Infrastructure

Run the bootstrap script to create core resources:

```bash
cd infrastructure
./aws-bootstrap.sh
```

This will create:
- IAM user for your AI assistant
- Secrets Manager secret store
- S3 bucket for backups
- Budget alarm

### 2. Store Your Secrets

Add API keys and credentials to Secrets Manager:

```bash
# Store a secret
aws secretsmanager create-secret \
  --name jarvis-ai/gmail-api-token \
  --secret-string "your-token-here" \
  --region us-east-1
```

Or use the helper script:

```bash
cd secrets-manager
./set-secret.sh jarvis-ai/gmail-api-token "your-token-here"
```

### 3. Set Up Backups

Configure automatic vault backups to S3:

```bash
cd s3
./vault-backup.sh /path/to/your/vault s3://your-backup-bucket
```

Add to cron for daily backups:

```bash
0 2 * * * /path/to/infrastructure/s3/vault-backup.sh /path/to/vault s3://your-backup-bucket
```

### 4. Deploy Lambda Functions (Optional)

If you need scheduled tasks or webhooks:

```bash
cd lambda/templates/cron-job
# Package your function
zip -r function.zip handler.py

# Deploy to Lambda
aws lambda create-function \
  --function-name daily-digest \
  --runtime python3.11 \
  --handler handler.lambda_handler \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --zip-file fileb://function.zip \
  --region us-east-1
```

### 5. Set Up Monitoring

Create budget alerts to avoid surprise bills:

```bash
cd monitoring
./alerts-setup.sh your-email@example.com
```

## Cost Expectations

**Free Tier Coverage** (first 12 months):

- Secrets Manager: First 30 days free, then $0.40/secret/month
- Lambda: 1M requests/month + 400,000 GB-seconds compute free
- S3: 5GB storage, 20,000 GET requests, 2,000 PUT requests free
- CloudWatch: 10 custom metrics, 10 alarms free

**Expected Monthly Cost for Personal Use**: $1-5/month after free tier

## Directory Structure

```
infrastructure/
├── README.md                    # This file
├── aws-bootstrap.sh             # Initial setup script
├── secrets-manager/
│   ├── README.md               # Secrets Manager guide
│   └── get-secret.py           # Helper to retrieve secrets
├── lambda/
│   ├── templates/
│   │   ├── cron-job/           # Scheduled task template
│   │   └── webhook/            # API Gateway webhook template
├── s3/
│   └── vault-backup.sh         # Vault backup script
└── monitoring/
    └── alerts-setup.sh         # Budget and alarm setup
```

## Security Best Practices

1. **Never commit secrets** - Use Secrets Manager, not environment variables
2. **Use IAM roles** - Grant minimum permissions needed
3. **Enable MFA** - Protect your AWS root account
4. **Rotate credentials** - Update API keys regularly
5. **Monitor costs** - Set up budget alerts
6. **Use encryption** - S3 encryption at rest is free

## Learn More

- [Secrets Manager Documentation](./secrets-manager/README.md)
- [Lambda Templates](./lambda/templates/)
- [S3 Backup Guide](./s3/)
- [Monitoring Setup](./monitoring/)

## Troubleshooting

### "Access Denied" errors

Your AWS user needs these IAM policies:
- `SecretsManagerReadWrite`
- `AWSLambda_FullAccess`
- `AmazonS3FullAccess`
- `CloudWatchFullAccess`

### "Credentials not configured"

Run `aws configure` and enter your access key ID and secret access key.

### Cost concerns

Start with the monitoring setup to get budget alerts. Most personal use cases stay under $5/month.

## Support

For issues with this scaffold:
1. Check the individual README files in each directory
2. Review AWS documentation
3. Open an issue in the repository

---

**Note**: This is a teaching scaffold for personal AI assistants. For production deployments, consider additional security hardening, infrastructure-as-code (CDK/Terraform), and proper CI/CD pipelines.
