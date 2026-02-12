#!/usr/bin/env bash

set -e

# AWS Monitoring Alerts Setup
# Creates budget alerts and CloudWatch alarms to monitor AWS costs and usage

# Usage:
#   ./alerts-setup.sh user@example.com
#   ./alerts-setup.sh user@example.com --budget 20
#   ./alerts-setup.sh user@example.com --dry-run

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Show usage
show_usage() {
    cat << EOF
AWS Monitoring Alerts Setup

Creates budget alerts to notify you before costs exceed your threshold.

Usage:
  $0 EMAIL [OPTIONS]

Arguments:
  EMAIL    Email address to receive alerts (required)

Options:
  --budget AMOUNT    Monthly budget in USD (default: 10)
  --threshold PCT    Alert threshold percentage (default: 80)
  --region REGION    AWS region (default: us-east-1)
  --profile PROFILE  AWS CLI profile to use
  --dry-run         Show what would be created without creating
  --help            Show this help message

Examples:
  # Create alerts with default $10 budget
  $0 user@example.com

  # Create alerts with custom budget
  $0 user@example.com --budget 20

  # Create alerts with 50% threshold (alert at $5 of $10)
  $0 user@example.com --budget 10 --threshold 50

  # Dry run to see what would be created
  $0 user@example.com --dry-run

What gets created:
  1. SNS topic for budget alerts
  2. SNS subscription (email confirmation required)
  3. Budget with 80% and 100% thresholds (manual setup in console)

Note: AWS Budgets API requires specific IAM permissions and may need
manual setup in the AWS Console: https://console.aws.amazon.com/billing/home#/budgets

EOF
}

# Parse arguments
EMAIL=""
BUDGET_AMOUNT="10"
ALERT_THRESHOLD="80"
AWS_REGION="us-east-1"
AWS_PROFILE=""
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --budget)
            BUDGET_AMOUNT="$2"
            shift 2
            ;;
        --threshold)
            ALERT_THRESHOLD="$2"
            shift 2
            ;;
        --region)
            AWS_REGION="$2"
            shift 2
            ;;
        --profile)
            AWS_PROFILE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="true"
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        -*)
            log_error "Unknown option: $1"
            echo ""
            show_usage
            exit 1
            ;;
        *)
            if [ -z "$EMAIL" ]; then
                EMAIL="$1"
            else
                log_error "Too many arguments"
                echo ""
                show_usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate required arguments
if [ -z "$EMAIL" ]; then
    log_error "Email address is required"
    echo ""
    show_usage
    exit 1
fi

# Validate email format (basic check)
if [[ ! "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    log_error "Invalid email address format: $EMAIL"
    exit 1
fi

# Check AWS CLI is installed
if ! command -v aws &> /dev/null; then
    log_error "AWS CLI is not installed. Install from: https://aws.amazon.com/cli/"
    exit 1
fi

# Build AWS CLI profile argument
PROFILE_ARG=""
if [ -n "$AWS_PROFILE" ]; then
    PROFILE_ARG="--profile $AWS_PROFILE"
fi

# Check AWS credentials
if ! aws sts get-caller-identity $PROFILE_ARG &> /dev/null; then
    log_error "AWS credentials not configured. Run: aws configure"
    exit 1
fi

# Get AWS account ID
ACCOUNT_ID=$(aws sts get-caller-identity $PROFILE_ARG --query Account --output text)

# Display setup info
echo ""
log_info "AWS Monitoring Alerts Setup"
echo ""
echo "  Email:       $EMAIL"
echo "  Budget:      \$$BUDGET_AMOUNT USD/month"
echo "  Threshold:   ${ALERT_THRESHOLD}% (\$$((BUDGET_AMOUNT * ALERT_THRESHOLD / 100)))"
echo "  Region:      $AWS_REGION"
echo "  Account:     $ACCOUNT_ID"
if [ -n "$AWS_PROFILE" ]; then
    echo "  Profile:     $AWS_PROFILE"
fi
if [ "$DRY_RUN" = "true" ]; then
    log_warning "DRY RUN MODE - No resources will be created"
fi
echo ""

# ─────────────────────────────────────────────────────────────────────
# 1. Create SNS Topic for Budget Alerts
# ─────────────────────────────────────────────────────────────────────

log_info "Step 1/3: Creating SNS topic for budget alerts..."

SNS_TOPIC_NAME="budget-alerts"

if [ "$DRY_RUN" = "true" ]; then
    log_warning "Would create SNS topic: $SNS_TOPIC_NAME"
    SNS_TOPIC_ARN="arn:aws:sns:$AWS_REGION:$ACCOUNT_ID:$SNS_TOPIC_NAME"
else
    # Check if topic already exists
    EXISTING_TOPIC=$(aws sns list-topics $PROFILE_ARG --region $AWS_REGION --output json | grep -o "arn:aws:sns:$AWS_REGION:$ACCOUNT_ID:$SNS_TOPIC_NAME" || echo "")

    if [ -n "$EXISTING_TOPIC" ]; then
        log_warning "SNS topic already exists: $SNS_TOPIC_NAME"
        SNS_TOPIC_ARN="$EXISTING_TOPIC"
    else
        # Create SNS topic
        SNS_TOPIC_ARN=$(aws sns create-topic \
            --name "$SNS_TOPIC_NAME" \
            --region "$AWS_REGION" \
            $PROFILE_ARG \
            --output text \
            --query TopicArn)

        log_success "Created SNS topic: $SNS_TOPIC_ARN"
    fi
fi

echo ""

# ─────────────────────────────────────────────────────────────────────
# 2. Subscribe Email to SNS Topic
# ─────────────────────────────────────────────────────────────────────

log_info "Step 2/3: Subscribing email to SNS topic..."

if [ "$DRY_RUN" = "true" ]; then
    log_warning "Would subscribe email: $EMAIL"
else
    # Check if subscription already exists
    EXISTING_SUB=$(aws sns list-subscriptions-by-topic \
        --topic-arn "$SNS_TOPIC_ARN" \
        --region "$AWS_REGION" \
        $PROFILE_ARG \
        --output json | grep -o "$EMAIL" || echo "")

    if [ -n "$EXISTING_SUB" ]; then
        log_warning "Email already subscribed: $EMAIL"
    else
        # Subscribe email to topic
        SUBSCRIPTION_ARN=$(aws sns subscribe \
            --topic-arn "$SNS_TOPIC_ARN" \
            --protocol email \
            --notification-endpoint "$EMAIL" \
            --region "$AWS_REGION" \
            $PROFILE_ARG \
            --output text \
            --query SubscriptionArn)

        log_success "Subscribed email: $EMAIL"
        log_warning "IMPORTANT: Check your email and confirm the subscription!"
        log_info "You must click the confirmation link in the email to receive alerts"
    fi
fi

echo ""

# ─────────────────────────────────────────────────────────────────────
# 3. Create Budget (Manual Step)
# ─────────────────────────────────────────────────────────────────────

log_info "Step 3/3: Setting up budget alerts..."

# Note: AWS Budgets API requires special permissions and is region-specific (us-east-1)
# For simplicity, we provide manual instructions

if [ "$DRY_RUN" = "true" ]; then
    log_warning "Would create budget with SNS notifications"
else
    log_warning "Budget creation requires manual setup in AWS Console"
    echo ""
    log_info "To complete budget alert setup:"
    echo ""
    echo "  1. Visit: https://console.aws.amazon.com/billing/home#/budgets"
    echo "  2. Click 'Create budget'"
    echo "  3. Choose 'Cost budget'"
    echo "  4. Set budget amount: \$$BUDGET_AMOUNT per month"
    echo "  5. Add alert thresholds:"
    echo "     - Alert at ${ALERT_THRESHOLD}% of budget"
    echo "     - Alert at 100% of budget"
    echo "  6. Configure notifications:"
    echo "     - SNS Topic ARN: $SNS_TOPIC_ARN"
    echo "     - Or use email: $EMAIL"
    echo ""
fi

echo ""

# ─────────────────────────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────────────────────────

if [ "$DRY_RUN" = "true" ]; then
    log_success "Dry run complete - no resources were created"
else
    log_success "Monitoring alerts setup complete!"
    echo ""
    log_info "What was created:"
    echo "  ✓ SNS Topic: $SNS_TOPIC_ARN"
    echo "  ✓ Email subscription: $EMAIL (confirmation pending)"
    echo ""
    log_warning "Next steps:"
    echo "  1. Check your email ($EMAIL) and confirm the SNS subscription"
    echo "  2. Set up budget alerts in AWS Console (see instructions above)"
    echo "  3. You'll receive email alerts when costs reach ${ALERT_THRESHOLD}% and 100% of budget"
    echo ""
    log_info "To test the alert system:"
    echo "  aws sns publish \\"
    echo "    --topic-arn $SNS_TOPIC_ARN \\"
    echo "    --message 'Test budget alert' \\"
    echo "    --region $AWS_REGION"
    echo ""
fi

exit 0
