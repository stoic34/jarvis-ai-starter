"""
AWS Lambda Handler - Scheduled Task (Cron Job)

This Lambda function runs on a schedule using EventBridge (CloudWatch Events).
Perfect for recurring tasks like daily digests, backups, or data processing.

Deployment:
    1. Zip this file: zip function.zip handler.py
    2. Create Lambda function via AWS CLI or Console
    3. Create EventBridge rule with schedule expression
    4. Add Lambda function as target

Schedule Examples (EventBridge cron expressions):
    Every hour:          rate(1 hour)
    Every day at 2am:    cron(0 2 * * ? *)
    Every weekday 9am:   cron(0 9 ? * MON-FRI *)
    First of month:      cron(0 0 1 * ? *)

Environment Variables:
    Set these in Lambda configuration:
    - VAULT_BACKUP_BUCKET: S3 bucket for vault backups
    - NOTIFICATION_EMAIL: Email for digest notifications
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR (default: INFO)
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level))


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler function - called by EventBridge on schedule.

    Args:
        event: EventBridge event payload (includes time, resources, etc.)
        context: Lambda runtime context (request ID, memory, etc.)

    Returns:
        Dict with statusCode, body, and metadata

    Example event payload from EventBridge:
    {
        "version": "0",
        "id": "abc123",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "time": "2024-01-01T02:00:00Z",
        "region": "us-east-1",
        "resources": ["arn:aws:events:us-east-1:123456789012:rule/daily-task"],
        "detail": {}
    }
    """
    # Log incoming event (useful for debugging)
    logger.info(f"Lambda invoked by EventBridge")
    logger.debug(f"Event: {json.dumps(event)}")
    logger.debug(f"Request ID: {context.request_id}")

    try:
        # Extract event details
        event_time = event.get("time", datetime.utcnow().isoformat())
        rule_name = extract_rule_name(event)

        logger.info(f"Running scheduled task: {rule_name} at {event_time}")

        # ─────────────────────────────────────────────────────────────
        # YOUR SCHEDULED TASK LOGIC GOES HERE
        # ─────────────────────────────────────────────────────────────

        # Example 1: Trigger a vault backup
        result = trigger_vault_backup()

        # Example 2: Generate and send a daily digest
        # result = generate_daily_digest()

        # Example 3: Process data or clean up old records
        # result = cleanup_old_records()

        # Example 4: Check external service and alert if needed
        # result = health_check_external_service()

        # ─────────────────────────────────────────────────────────────

        logger.info(f"Task completed successfully: {result['message']}")

        # Return success response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Scheduled task completed successfully",
                "rule": rule_name,
                "timestamp": event_time,
                "result": result,
            }),
        }

    except Exception as e:
        logger.error(f"Task failed: {str(e)}", exc_info=True)

        # Return error response
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Scheduled task failed",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }),
        }


def extract_rule_name(event: Dict[str, Any]) -> str:
    """Extract the EventBridge rule name from the event."""
    resources = event.get("resources", [])
    if resources:
        # ARN format: arn:aws:events:region:account:rule/rule-name
        rule_arn = resources[0]
        return rule_arn.split("/")[-1]
    return "unknown"


# ─────────────────────────────────────────────────────────────────────
# EXAMPLE TASK IMPLEMENTATIONS
# ─────────────────────────────────────────────────────────────────────


def trigger_vault_backup() -> Dict[str, Any]:
    """
    Example: Trigger a vault backup to S3.

    In a real implementation:
    1. Read vault files from local storage or EFS
    2. Compress vault directory
    3. Upload to S3 with timestamp
    4. Send notification on completion
    """
    import boto3

    bucket_name = os.environ.get("VAULT_BACKUP_BUCKET")

    if not bucket_name:
        raise ValueError("VAULT_BACKUP_BUCKET environment variable not set")

    # Example: Create a backup marker file
    s3 = boto3.client("s3")
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    marker_key = f"backups/vault-backup-{timestamp}.marker"

    s3.put_object(
        Bucket=bucket_name,
        Key=marker_key,
        Body=json.dumps({
            "timestamp": timestamp,
            "status": "backup_triggered",
            "lambda_request_id": "example-request-id",
        }),
        ContentType="application/json",
    )

    logger.info(f"Backup triggered: s3://{bucket_name}/{marker_key}")

    return {
        "message": "Vault backup triggered successfully",
        "backup_location": f"s3://{bucket_name}/{marker_key}",
        "timestamp": timestamp,
    }


def generate_daily_digest() -> Dict[str, Any]:
    """
    Example: Generate a daily digest email.

    In a real implementation:
    1. Query database for today's activities
    2. Fetch unread notifications
    3. Generate summary statistics
    4. Send email via SES or SNS
    """
    # Placeholder implementation
    logger.info("Generating daily digest...")

    # Example: Count items processed
    items_processed = 42
    notifications = 7
    tasks_completed = 5

    # Example: Send notification (requires SNS topic ARN)
    notification_email = os.environ.get("NOTIFICATION_EMAIL")

    if notification_email:
        logger.info(f"Would send digest to: {notification_email}")
        # In production: Use boto3 SES or SNS to send email

    return {
        "message": "Daily digest generated",
        "items_processed": items_processed,
        "notifications": notifications,
        "tasks_completed": tasks_completed,
    }


def cleanup_old_records() -> Dict[str, Any]:
    """
    Example: Clean up old records from DynamoDB or S3.

    In a real implementation:
    1. Query for records older than retention period
    2. Delete expired items
    3. Log cleanup statistics
    """
    # Placeholder implementation
    logger.info("Cleaning up old records...")

    # Example: Delete items older than 90 days
    retention_days = 90
    deleted_count = 15

    logger.info(f"Deleted {deleted_count} records older than {retention_days} days")

    return {
        "message": "Cleanup completed",
        "deleted_count": deleted_count,
        "retention_days": retention_days,
    }


def health_check_external_service() -> Dict[str, Any]:
    """
    Example: Check health of an external service and alert if down.

    In a real implementation:
    1. Make HTTP request to health endpoint
    2. Validate response
    3. Send alert via SNS if unhealthy
    """
    import urllib.request

    # Placeholder implementation
    logger.info("Checking external service health...")

    # Example: Check a public endpoint
    try:
        response = urllib.request.urlopen("https://www.example.com", timeout=5)
        status_code = response.getcode()

        if status_code == 200:
            logger.info("External service is healthy")
            return {
                "message": "Health check passed",
                "status_code": status_code,
                "healthy": True,
            }
        else:
            logger.warning(f"External service returned status {status_code}")
            # In production: Send alert via SNS
            return {
                "message": "Health check warning",
                "status_code": status_code,
                "healthy": False,
            }

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        # In production: Send alert via SNS
        return {
            "message": "Health check failed",
            "error": str(e),
            "healthy": False,
        }


# ─────────────────────────────────────────────────────────────────────
# LOCAL TESTING
# ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    """
    Local testing - simulates EventBridge invocation.

    Run: python handler.py
    """
    # Mock EventBridge event
    test_event = {
        "version": "0",
        "id": "test-event-123",
        "detail-type": "Scheduled Event",
        "source": "aws.events",
        "time": datetime.utcnow().isoformat(),
        "region": "us-east-1",
        "resources": ["arn:aws:events:us-east-1:123456789012:rule/daily-backup"],
        "detail": {},
    }

    # Mock Lambda context
    class MockContext:
        request_id = "test-request-123"
        function_name = "daily-backup-handler"
        memory_limit_in_mb = 128

    # Set test environment variables
    os.environ["VAULT_BACKUP_BUCKET"] = "test-backup-bucket"
    os.environ["NOTIFICATION_EMAIL"] = "test@example.com"
    os.environ["LOG_LEVEL"] = "DEBUG"

    # Invoke handler
    print("=" * 60)
    print("LOCAL TESTING - Simulating EventBridge invocation")
    print("=" * 60)

    result = lambda_handler(test_event, MockContext())

    print("\nResponse:")
    print(json.dumps(result, indent=2))
