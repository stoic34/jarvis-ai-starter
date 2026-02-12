"""
AWS Lambda Handler - API Gateway Webhook

This Lambda function receives HTTP requests from API Gateway.
Perfect for webhooks from external services (Slack, Shopify, GitHub, etc.)

Deployment:
    1. Zip this file: zip function.zip handler.py
    2. Create Lambda function via AWS CLI or Console
    3. Create API Gateway (HTTP API or REST API)
    4. Add Lambda function as integration target
    5. Configure webhook in external service with API Gateway URL

Environment Variables:
    Set these in Lambda configuration:
    - WEBHOOK_SECRET: Secret token for request validation
    - ALLOWED_ORIGINS: Comma-separated CORS origins (optional)
    - LOG_LEVEL: DEBUG, INFO, WARNING, ERROR (default: INFO)

API Gateway URL Format:
    https://{api-id}.execute-api.{region}.amazonaws.com/{stage}/webhook
"""

import hashlib
import hmac
import json
import logging
import os
from typing import Dict, Any, Optional

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger = logging.getLogger()
logger.setLevel(getattr(logging, log_level))


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler function - called by API Gateway on HTTP request.

    Args:
        event: API Gateway event payload (includes headers, body, method, etc.)
        context: Lambda runtime context (request ID, memory, etc.)

    Returns:
        Dict with statusCode, body, and headers

    Example event payload from API Gateway:
    {
        "version": "2.0",
        "routeKey": "POST /webhook",
        "rawPath": "/webhook",
        "requestContext": {
            "http": {
                "method": "POST",
                "path": "/webhook",
                "sourceIp": "203.0.113.1"
            }
        },
        "headers": {
            "content-type": "application/json",
            "x-webhook-signature": "sha256=abc123..."
        },
        "body": "{\"event\":\"test\",\"data\":{}}",
        "isBase64Encoded": false
    }
    """
    # Log incoming request
    logger.info(f"Webhook received from {get_source_ip(event)}")
    logger.debug(f"Event: {json.dumps(event)}")
    logger.debug(f"Request ID: {context.request_id}")

    try:
        # Extract request details
        http_method = get_http_method(event)
        path = get_path(event)
        headers = event.get("headers", {})
        body = event.get("body", "")

        logger.info(f"{http_method} {path}")

        # Parse request body
        if body:
            # Handle base64 encoded body
            if event.get("isBase64Encoded", False):
                import base64
                body = base64.b64decode(body).decode("utf-8")

            # Parse JSON body
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                logger.warning("Request body is not valid JSON")
                return error_response(400, "Invalid JSON in request body")
        else:
            payload = {}

        # Validate webhook signature (if secret is configured)
        webhook_secret = os.environ.get("WEBHOOK_SECRET")
        if webhook_secret:
            signature = headers.get("x-webhook-signature") or headers.get("x-hub-signature-256")
            if not signature:
                logger.warning("Missing webhook signature")
                return error_response(401, "Missing signature")

            if not verify_signature(body, signature, webhook_secret):
                logger.error("Invalid webhook signature")
                return error_response(401, "Invalid signature")

        # ─────────────────────────────────────────────────────────────
        # YOUR WEBHOOK LOGIC GOES HERE
        # ─────────────────────────────────────────────────────────────

        # Example: Process webhook from different services
        result = process_webhook(payload, headers)

        # ─────────────────────────────────────────────────────────────

        logger.info(f"Webhook processed successfully: {result['message']}")

        # Return success response with CORS headers
        return success_response(result)

    except Exception as e:
        logger.error(f"Webhook processing failed: {str(e)}", exc_info=True)
        return error_response(500, f"Internal server error: {str(e)}")


# ─────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────


def get_http_method(event: Dict[str, Any]) -> str:
    """Extract HTTP method from API Gateway event."""
    # API Gateway v2 format
    if "requestContext" in event and "http" in event["requestContext"]:
        return event["requestContext"]["http"]["method"]
    # API Gateway v1 format
    return event.get("httpMethod", "UNKNOWN")


def get_path(event: Dict[str, Any]) -> str:
    """Extract request path from API Gateway event."""
    # API Gateway v2 format
    if "rawPath" in event:
        return event["rawPath"]
    # API Gateway v1 format
    return event.get("path", "/")


def get_source_ip(event: Dict[str, Any]) -> str:
    """Extract source IP from API Gateway event."""
    # API Gateway v2 format
    if "requestContext" in event and "http" in event["requestContext"]:
        return event["requestContext"]["http"]["sourceIp"]
    # API Gateway v1 format
    if "requestContext" in event:
        return event["requestContext"].get("identity", {}).get("sourceIp", "unknown")
    return "unknown"


def verify_signature(body: str, signature: str, secret: str) -> bool:
    """
    Verify webhook signature (HMAC SHA256).

    Common signature formats:
    - GitHub: sha256=<hex_digest>
    - Shopify: <hex_digest>
    - Slack: v0=<hex_digest>

    Args:
        body: Raw request body (string)
        signature: Signature from request header
        secret: Webhook secret for HMAC

    Returns:
        True if signature is valid, False otherwise
    """
    # Remove signature prefix if present (e.g., "sha256=")
    if "=" in signature:
        signature = signature.split("=", 1)[1]

    # Compute expected signature
    expected = hmac.new(
        key=secret.encode("utf-8"),
        msg=body.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()

    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected, signature)


def success_response(data: Any, status_code: int = 200) -> Dict[str, Any]:
    """Build a success HTTP response with CORS headers."""
    return {
        "statusCode": status_code,
        "headers": get_cors_headers(),
        "body": json.dumps(data),
    }


def error_response(status_code: int, message: str) -> Dict[str, Any]:
    """Build an error HTTP response with CORS headers."""
    return {
        "statusCode": status_code,
        "headers": get_cors_headers(),
        "body": json.dumps({
            "error": message,
            "statusCode": status_code,
        }),
    }


def get_cors_headers() -> Dict[str, str]:
    """Get CORS headers for API responses."""
    allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")

    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": allowed_origins,
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,X-Webhook-Signature,Authorization",
    }


# ─────────────────────────────────────────────────────────────────────
# WEBHOOK PROCESSING LOGIC
# ─────────────────────────────────────────────────────────────────────


def process_webhook(payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Process incoming webhook payload.

    Args:
        payload: Parsed JSON payload from webhook
        headers: Request headers (lowercase keys in API Gateway v2)

    Returns:
        Dict with processing result

    Example webhooks to handle:
    - GitHub: push events, PR events
    - Shopify: order created, product updated
    - Slack: slash commands, interactive components
    - Stripe: payment succeeded, subscription updated
    """
    # Detect webhook source from headers or payload
    webhook_source = detect_webhook_source(headers, payload)

    logger.info(f"Processing webhook from: {webhook_source}")

    # Route to appropriate handler based on source
    if webhook_source == "github":
        return handle_github_webhook(payload, headers)
    elif webhook_source == "shopify":
        return handle_shopify_webhook(payload, headers)
    elif webhook_source == "slack":
        return handle_slack_webhook(payload, headers)
    else:
        return handle_generic_webhook(payload)


def detect_webhook_source(headers: Dict[str, str], payload: Dict[str, Any]) -> str:
    """Detect webhook source from headers or payload."""
    # Check common webhook headers (API Gateway lowercases header names)
    if "x-github-event" in headers:
        return "github"
    elif "x-shopify-topic" in headers:
        return "shopify"
    elif "x-slack-signature" in headers:
        return "slack"

    # Check payload structure
    if "action" in payload and "repository" in payload:
        return "github"
    elif "id" in payload and "admin_graphql_api_id" in payload:
        return "shopify"

    return "generic"


def handle_github_webhook(payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Handle GitHub webhook events.

    Common events: push, pull_request, issues, release, etc.
    """
    event_type = headers.get("x-github-event", "unknown")

    logger.info(f"GitHub event: {event_type}")

    # Example: Handle push event
    if event_type == "push":
        ref = payload.get("ref", "")
        commits = payload.get("commits", [])
        repository = payload.get("repository", {}).get("full_name", "unknown")

        logger.info(f"Push to {repository} ({ref}): {len(commits)} commits")

        # Your logic here: trigger CI/CD, notify team, update status, etc.

        return {
            "message": "GitHub push event processed",
            "repository": repository,
            "ref": ref,
            "commit_count": len(commits),
        }

    # Example: Handle pull request event
    elif event_type == "pull_request":
        action = payload.get("action", "unknown")
        pr_number = payload.get("pull_request", {}).get("number", 0)
        title = payload.get("pull_request", {}).get("title", "")

        logger.info(f"Pull request #{pr_number}: {action} - {title}")

        # Your logic here: run checks, post comments, assign reviewers, etc.

        return {
            "message": "GitHub PR event processed",
            "action": action,
            "pr_number": pr_number,
        }

    return {
        "message": f"GitHub {event_type} event received",
        "event": event_type,
    }


def handle_shopify_webhook(payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Handle Shopify webhook events.

    Common topics: orders/create, products/update, customers/create, etc.
    """
    topic = headers.get("x-shopify-topic", "unknown")
    shop_domain = headers.get("x-shopify-shop-domain", "unknown")

    logger.info(f"Shopify event: {topic} from {shop_domain}")

    # Example: Handle new order
    if topic == "orders/create":
        order_id = payload.get("id")
        total_price = payload.get("total_price")
        customer = payload.get("customer", {})

        logger.info(f"New order #{order_id}: ${total_price}")

        # Your logic here: send confirmation, update inventory, notify fulfillment, etc.

        return {
            "message": "Shopify order created",
            "order_id": order_id,
            "total_price": total_price,
        }

    return {
        "message": f"Shopify {topic} event received",
        "topic": topic,
        "shop": shop_domain,
    }


def handle_slack_webhook(payload: Dict[str, Any], headers: Dict[str, str]) -> Dict[str, Any]:
    """
    Handle Slack webhook events (slash commands, interactive components).
    """
    # Slack sends URL-encoded form data, not JSON
    # In production, parse form data: urllib.parse.parse_qs(body)

    event_type = payload.get("type", "unknown")

    logger.info(f"Slack event: {event_type}")

    # Example: Handle slash command
    if event_type == "slash_command":
        command = payload.get("command")
        text = payload.get("text")
        user_id = payload.get("user_id")

        logger.info(f"Slash command from {user_id}: {command} {text}")

        # Your logic here: process command, query data, trigger action, etc.

        return {
            "response_type": "in_channel",
            "text": f"Received command: {command} {text}",
        }

    return {
        "message": f"Slack {event_type} event received",
        "type": event_type,
    }


def handle_generic_webhook(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handle generic webhook (unknown source)."""
    logger.info(f"Generic webhook payload: {json.dumps(payload)[:200]}")

    # Your logic here: log, store, forward, etc.

    return {
        "message": "Webhook received and processed",
        "payload_keys": list(payload.keys()),
    }


# ─────────────────────────────────────────────────────────────────────
# LOCAL TESTING
# ─────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    """
    Local testing - simulates API Gateway invocation.

    Run: python handler.py
    """
    # Mock API Gateway event
    test_event = {
        "version": "2.0",
        "routeKey": "POST /webhook",
        "rawPath": "/webhook",
        "requestContext": {
            "http": {
                "method": "POST",
                "path": "/webhook",
                "sourceIp": "203.0.113.1",
            }
        },
        "headers": {
            "content-type": "application/json",
            "x-github-event": "push",
        },
        "body": json.dumps({
            "ref": "refs/heads/main",
            "commits": [
                {"id": "abc123", "message": "Test commit"}
            ],
            "repository": {
                "full_name": "user/repo"
            }
        }),
        "isBase64Encoded": False,
    }

    # Mock Lambda context
    class MockContext:
        request_id = "test-request-123"
        function_name = "webhook-handler"
        memory_limit_in_mb = 128

    # Set test environment variables
    os.environ["LOG_LEVEL"] = "DEBUG"
    # os.environ["WEBHOOK_SECRET"] = "test-secret-123"

    # Invoke handler
    print("=" * 60)
    print("LOCAL TESTING - Simulating API Gateway invocation")
    print("=" * 60)

    result = lambda_handler(test_event, MockContext())

    print("\nResponse:")
    print(json.dumps(result, indent=2))
