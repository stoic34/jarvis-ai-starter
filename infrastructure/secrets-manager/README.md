# AWS Secrets Manager

AWS Secrets Manager provides secure, encrypted storage for sensitive credentials like API keys, tokens, and passwords. This is the recommended way to store secrets for your AI assistant.

## Why Use Secrets Manager?

**Never store secrets in code or environment variables.** Here's why Secrets Manager is better:

- **Encrypted at rest** - Secrets are encrypted using AWS KMS
- **Audit trail** - Every access to a secret is logged in CloudTrail
- **Rotation support** - Automatically rotate credentials on a schedule
- **Access control** - Use IAM policies to control who can read secrets
- **No accidental commits** - Secrets never touch your codebase

## When to Use Secrets Manager

Store these types of credentials in Secrets Manager:

- API keys (Gmail, Slack, Shopify, etc.)
- OAuth tokens and refresh tokens
- Database passwords
- Third-party service credentials
- Webhook signing secrets

## Cost

- **Free tier**: 30 days free for new secrets
- **After free tier**: $0.40 per secret per month
- **API calls**: $0.05 per 10,000 calls

For a typical AI assistant with 5-10 secrets, expect ~$2-4/month.

## Quick Start

### 1. Create a Secret

```bash
# Simple string secret
aws secretsmanager create-secret \
  --name jarvis-ai/gmail-api-token \
  --description "Gmail API OAuth token" \
  --secret-string "ya29.a0AfH6SMBx..." \
  --region us-east-1

# JSON secret (for multiple values)
aws secretsmanager create-secret \
  --name jarvis-ai/database \
  --description "Database credentials" \
  --secret-string '{"username":"admin","password":"secret123"}' \
  --region us-east-1
```

### 2. Retrieve a Secret

```bash
# Get the secret value
aws secretsmanager get-secret-value \
  --secret-id jarvis-ai/gmail-api-token \
  --region us-east-1 \
  --query SecretString \
  --output text

# Or use the helper script
./get-secret.py --name jarvis-ai/gmail-api-token
```

### 3. Update a Secret

```bash
# Update existing secret
aws secretsmanager put-secret-value \
  --secret-id jarvis-ai/gmail-api-token \
  --secret-string "new-token-value" \
  --region us-east-1
```

### 4. Delete a Secret

```bash
# Schedule deletion (7-30 day recovery window)
aws secretsmanager delete-secret \
  --secret-id jarvis-ai/gmail-api-token \
  --recovery-window-in-days 7 \
  --region us-east-1

# Cancel deletion (if within recovery window)
aws secretsmanager restore-secret \
  --secret-id jarvis-ai/gmail-api-token \
  --region us-east-1
```

## Using Secrets in Your AI Assistant

### Python Example

```python
import boto3
import json

def get_secret(secret_name, region="us-east-1"):
    """Retrieve a secret from AWS Secrets Manager."""
    client = boto3.client('secretsmanager', region_name=region)

    try:
        response = client.get_secret_value(SecretId=secret_name)

        # Parse JSON secrets
        if 'SecretString' in response:
            secret = response['SecretString']
            try:
                return json.loads(secret)
            except json.JSONDecodeError:
                return secret

        # Handle binary secrets
        return response['SecretBinary']

    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

# Usage
gmail_token = get_secret("jarvis-ai/gmail-api-token")
db_creds = get_secret("jarvis-ai/database")  # Returns dict
```

### Node.js Example

```javascript
const { SecretsManagerClient, GetSecretValueCommand } = require("@aws-sdk/client-secrets-manager");

async function getSecret(secretName, region = "us-east-1") {
  const client = new SecretsManagerClient({ region });

  try {
    const response = await client.send(
      new GetSecretValueCommand({ SecretId: secretName })
    );

    // Parse JSON secrets
    if (response.SecretString) {
      try {
        return JSON.parse(response.SecretString);
      } catch {
        return response.SecretString;
      }
    }

    return response.SecretBinary;
  } catch (error) {
    console.error(`Error retrieving secret ${secretName}:`, error);
    throw error;
  }
}

// Usage
const gmailToken = await getSecret("jarvis-ai/gmail-api-token");
const dbCreds = await getSecret("jarvis-ai/database");
```

### Shell Script Example

```bash
#!/bin/bash

# Function to get secret
get_secret() {
    local secret_name=$1
    local region=${2:-us-east-1}

    aws secretsmanager get-secret-value \
        --secret-id "$secret_name" \
        --region "$region" \
        --query SecretString \
        --output text
}

# Usage
GMAIL_TOKEN=$(get_secret "jarvis-ai/gmail-api-token")
echo "Retrieved token: ${GMAIL_TOKEN:0:10}..."
```

## Helper Script

Use `get-secret.py` for quick access:

```bash
# Get a secret
./get-secret.py --name jarvis-ai/gmail-api-token

# Get full response as JSON
./get-secret.py --name jarvis-ai/gmail-api-token --json

# Use a different region
./get-secret.py --name jarvis-ai/gmail-api-token --region us-west-2

# Use a specific AWS profile
./get-secret.py --name jarvis-ai/gmail-api-token --profile personal
```

## Organizing Secrets

Use a consistent naming convention:

```
project-name/service/credential-type

Examples:
  jarvis-ai/gmail/oauth-token
  jarvis-ai/slack/bot-token
  jarvis-ai/shopify/api-key
  jarvis-ai/database/password
```

## Secret Rotation

For sensitive credentials, enable automatic rotation:

```bash
# Create a Lambda function that rotates the secret
# Then attach it to the secret

aws secretsmanager rotate-secret \
  --secret-id jarvis-ai/database \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789012:function:rotate-db-password \
  --rotation-rules AutomaticallyAfterDays=30 \
  --region us-east-1
```

## Security Best Practices

1. **Use IAM policies** - Grant least privilege access
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "secretsmanager:GetSecretValue"
         ],
         "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:jarvis-ai/*"
       }
     ]
   }
   ```

2. **Enable CloudTrail** - Audit secret access

3. **Use resource tags** - Tag secrets for organization
   ```bash
   aws secretsmanager tag-resource \
     --secret-id jarvis-ai/gmail-api-token \
     --tags Key=Project,Value=jarvis-ai Key=Environment,Value=production
   ```

4. **Rotate regularly** - Change credentials every 30-90 days

5. **Monitor access** - Set up CloudWatch alarms for unusual access patterns

## Troubleshooting

### "ResourceNotFoundException"

The secret doesn't exist. Check:
- Secret name is correct (case-sensitive)
- Using the correct region
- Secret wasn't deleted

### "AccessDeniedException"

Your IAM user/role doesn't have permission. Attach this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret"
      ],
      "Resource": "*"
    }
  ]
}
```

### "InvalidRequestException"

Check your AWS CLI version:
```bash
aws --version
# Upgrade if needed
pip install --upgrade awscli
```

## Further Reading

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/)
- [Best Practices for Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html)
- [Secrets Manager Pricing](https://aws.amazon.com/secrets-manager/pricing/)
