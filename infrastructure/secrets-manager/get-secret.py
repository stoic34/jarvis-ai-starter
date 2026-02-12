#!/usr/bin/env python3
"""
AWS Secrets Manager Helper Script

Retrieves secrets from AWS Secrets Manager with a simple interface.

Usage:
    ./get-secret.py --name jarvis-ai/gmail-api-token
    ./get-secret.py --name jarvis-ai/database --json
    ./get-secret.py --name jarvis-ai/slack-token --region us-west-2
    ./get-secret.py --name jarvis-ai/api-key --profile personal

Examples:
    # Get a secret and use it in a script
    API_KEY=$(./get-secret.py --name jarvis-ai/api-key)
    echo "API Key: $API_KEY"

    # Get a JSON secret and parse with jq
    ./get-secret.py --name jarvis-ai/database --json | jq -r '.username'

    # Use in Python
    import subprocess
    token = subprocess.check_output(["./get-secret.py", "--name", "jarvis-ai/token"]).decode().strip()
"""

import argparse
import json
import sys
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name: str, region: str, profile: str = None) -> dict:
    """
    Retrieve a secret from AWS Secrets Manager.

    Args:
        secret_name: Name or ARN of the secret
        region: AWS region (e.g., us-east-1)
        profile: AWS CLI profile to use (optional)

    Returns:
        dict with 'value' (string or dict) and 'metadata' keys

    Raises:
        ClientError: If secret retrieval fails
    """
    # Create Secrets Manager client
    session_kwargs = {"region_name": region}
    if profile:
        session_kwargs["profile_name"] = profile

    session = boto3.Session(**session_kwargs)
    client = session.client("secretsmanager")

    try:
        # Get secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Extract the secret
        if "SecretString" in response:
            secret_string = response["SecretString"]

            # Try to parse as JSON
            try:
                secret_value = json.loads(secret_string)
            except json.JSONDecodeError:
                # Not JSON, return as plain string
                secret_value = secret_string
        else:
            # Binary secret (rare)
            secret_value = response["SecretBinary"].decode("utf-8")

        # Return both value and metadata
        return {
            "value": secret_value,
            "metadata": {
                "name": response.get("Name"),
                "arn": response.get("ARN"),
                "version_id": response.get("VersionId"),
                "created_date": response.get("CreatedDate").isoformat() if response.get("CreatedDate") else None,
            },
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "ResourceNotFoundException":
            print(f"Error: Secret '{secret_name}' not found in region '{region}'", file=sys.stderr)
            print(f"Check that the secret name is correct and exists in this region.", file=sys.stderr)
        elif error_code == "InvalidRequestException":
            print(f"Error: Invalid request for secret '{secret_name}'", file=sys.stderr)
        elif error_code == "InvalidParameterException":
            print(f"Error: Invalid parameter when retrieving secret '{secret_name}'", file=sys.stderr)
        elif error_code == "DecryptionFailure":
            print(f"Error: Could not decrypt secret '{secret_name}'", file=sys.stderr)
            print(f"Check that you have permission to use the KMS key.", file=sys.stderr)
        elif error_code == "AccessDeniedException":
            print(f"Error: Access denied to secret '{secret_name}'", file=sys.stderr)
            print(f"Your IAM user/role needs the 'secretsmanager:GetSecretValue' permission.", file=sys.stderr)
        else:
            print(f"Error: {error_code} - {e.response['Error']['Message']}", file=sys.stderr)

        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve secrets from AWS Secrets Manager",
        epilog="""
Examples:
  %(prog)s --name jarvis-ai/gmail-api-token
  %(prog)s --name jarvis-ai/database --json
  %(prog)s --name jarvis-ai/slack-token --region us-west-2 --profile personal

For more information, see: infrastructure/secrets-manager/README.md
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Name or ARN of the secret (e.g., jarvis-ai/gmail-api-token)",
    )

    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)",
    )

    parser.add_argument(
        "--profile",
        help="AWS CLI profile to use (optional)",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full response as JSON (includes metadata)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress all output except the secret value",
    )

    args = parser.parse_args()

    # Retrieve secret
    if not args.quiet:
        print(f"Retrieving secret: {args.name}", file=sys.stderr)

    result = get_secret(args.name, args.region, args.profile)

    # Output based on format
    if args.json:
        # Full response with metadata
        output = {
            "secret": result["value"],
            "metadata": result["metadata"],
        }
        print(json.dumps(output, indent=2))
    else:
        # Just the secret value
        if isinstance(result["value"], dict):
            # JSON secret - output as formatted JSON
            print(json.dumps(result["value"], indent=2))
        else:
            # Plain string secret
            print(result["value"])

    if not args.quiet:
        print(f"\nSuccessfully retrieved secret from region: {args.region}", file=sys.stderr)


if __name__ == "__main__":
    main()
