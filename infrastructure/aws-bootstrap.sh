#!/usr/bin/env bash

set -e

# AWS Infrastructure Bootstrap Script
# Creates core AWS resources for your AI assistant

# Configuration
PROJECT_NAME="${PROJECT_NAME:-jarvis-ai}"
AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_PROFILE="${AWS_PROFILE:-default}"
BUDGET_AMOUNT="${BUDGET_AMOUNT:-10}"
DRY_RUN="${DRY_RUN:-false}"

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

dry_run_check() {
    if [ "$DRY_RUN" = "true" ]; then
        log_warning "DRY RUN: Would execute: $1"
        return 1
    fi
    return 0
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Install from: https://aws.amazon.com/cli/"
        exit 1
    fi
    log_success "AWS CLI is installed"

    # Check AWS credentials
    if ! aws sts get-caller-identity --profile "$AWS_PROFILE" &> /dev/null; then
        log_error "AWS credentials not configured. Run: aws configure --profile $AWS_PROFILE"
        exit 1
    fi

    ACCOUNT_ID=$(aws sts get-caller-identity --profile "$AWS_PROFILE" --query Account --output text)
    log_success "AWS credentials configured (Account: $ACCOUNT_ID)"

    # Verify region
    log_info "Using region: $AWS_REGION"
}

# Create IAM user for AI assistant
create_iam_user() {
    log_info "Creating IAM user: ${PROJECT_NAME}-assistant..."

    USER_NAME="${PROJECT_NAME}-assistant"

    if dry_run_check "aws iam create-user --user-name $USER_NAME"; then
        if aws iam get-user --user-name "$USER_NAME" --profile "$AWS_PROFILE" &> /dev/null; then
            log_warning "IAM user '$USER_NAME' already exists, skipping..."
        else
            aws iam create-user \
                --user-name "$USER_NAME" \
                --profile "$AWS_PROFILE" \
                --tags "Key=Project,Value=$PROJECT_NAME" "Key=Purpose,Value=AI-Assistant"

            log_success "Created IAM user: $USER_NAME"
        fi
    fi

    # Create access key
    log_info "Creating access key for IAM user..."

    if dry_run_check "aws iam create-access-key --user-name $USER_NAME"; then
        ACCESS_KEY_OUTPUT=$(aws iam create-access-key \
            --user-name "$USER_NAME" \
            --profile "$AWS_PROFILE" \
            --output json 2>/dev/null || echo "")

        if [ -n "$ACCESS_KEY_OUTPUT" ]; then
            ACCESS_KEY_ID=$(echo "$ACCESS_KEY_OUTPUT" | grep -o '"AccessKeyId": "[^"]*"' | cut -d'"' -f4)
            SECRET_ACCESS_KEY=$(echo "$ACCESS_KEY_OUTPUT" | grep -o '"SecretAccessKey": "[^"]*"' | cut -d'"' -f4)

            log_success "Created access key"
            log_warning "SAVE THESE CREDENTIALS - They will not be shown again:"
            echo ""
            echo "  AWS_ACCESS_KEY_ID=$ACCESS_KEY_ID"
            echo "  AWS_SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY"
            echo ""
        else
            log_warning "Access key may already exist for this user"
        fi
    fi

    # Attach policies
    log_info "Attaching IAM policies..."

    POLICIES=(
        "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
        "arn:aws:iam::aws:policy/AmazonS3FullAccess"
        "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
    )

    for policy in "${POLICIES[@]}"; do
        if dry_run_check "aws iam attach-user-policy --user-name $USER_NAME --policy-arn $policy"; then
            aws iam attach-user-policy \
                --user-name "$USER_NAME" \
                --policy-arn "$policy" \
                --profile "$AWS_PROFILE" 2>/dev/null || log_warning "Policy may already be attached: $policy"
        fi
    done

    log_success "IAM user configured with necessary permissions"
}

# Create Secrets Manager secret store
create_secrets_store() {
    log_info "Creating Secrets Manager secret store..."

    SECRET_NAME="${PROJECT_NAME}/config"

    if dry_run_check "aws secretsmanager create-secret --name $SECRET_NAME"; then
        if aws secretsmanager describe-secret --secret-id "$SECRET_NAME" --region "$AWS_REGION" --profile "$AWS_PROFILE" &> /dev/null; then
            log_warning "Secret '$SECRET_NAME' already exists, skipping..."
        else
            aws secretsmanager create-secret \
                --name "$SECRET_NAME" \
                --description "Configuration secrets for $PROJECT_NAME AI assistant" \
                --secret-string '{}' \
                --region "$AWS_REGION" \
                --profile "$AWS_PROFILE"

            log_success "Created secret store: $SECRET_NAME"
        fi
    fi
}

# Create S3 bucket for backups
create_s3_bucket() {
    log_info "Creating S3 bucket for backups..."

    BUCKET_NAME="${PROJECT_NAME}-backups-${ACCOUNT_ID}"

    if dry_run_check "aws s3 mb s3://$BUCKET_NAME"; then
        if aws s3 ls "s3://$BUCKET_NAME" --profile "$AWS_PROFILE" &> /dev/null 2>&1; then
            log_warning "S3 bucket 's3://$BUCKET_NAME' already exists, skipping..."
        else
            # Create bucket
            if [ "$AWS_REGION" = "us-east-1" ]; then
                aws s3 mb "s3://$BUCKET_NAME" \
                    --profile "$AWS_PROFILE"
            else
                aws s3 mb "s3://$BUCKET_NAME" \
                    --region "$AWS_REGION" \
                    --profile "$AWS_PROFILE"
            fi

            log_success "Created S3 bucket: $BUCKET_NAME"

            # Enable versioning
            aws s3api put-bucket-versioning \
                --bucket "$BUCKET_NAME" \
                --versioning-configuration Status=Enabled \
                --profile "$AWS_PROFILE"

            log_success "Enabled versioning on S3 bucket"

            # Enable encryption
            aws s3api put-bucket-encryption \
                --bucket "$BUCKET_NAME" \
                --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}' \
                --profile "$AWS_PROFILE"

            log_success "Enabled encryption on S3 bucket"
        fi
    fi
}

# Set up budget alarm
setup_budget_alarm() {
    log_info "Setting up budget alarm ($BUDGET_AMOUNT USD/month)..."

    # Check if Budgets API is available (requires specific permissions)
    if ! aws budgets describe-budgets --account-id "$ACCOUNT_ID" --profile "$AWS_PROFILE" &> /dev/null; then
        log_warning "Cannot access AWS Budgets API. You may need to set up budget alarms manually in the AWS Console."
        log_info "Visit: https://console.aws.amazon.com/billing/home#/budgets"
        return
    fi

    BUDGET_NAME="${PROJECT_NAME}-monthly-budget"

    if dry_run_check "aws budgets create-budget --account-id $ACCOUNT_ID --budget file://budget.json"; then
        log_warning "Budget creation requires manual setup or additional permissions."
        log_info "To create a budget alarm manually:"
        echo "  1. Visit: https://console.aws.amazon.com/billing/home#/budgets"
        echo "  2. Create a monthly cost budget for \$$BUDGET_AMOUNT"
        echo "  3. Set alert threshold at 80% and 100%"
    fi
}

# Print summary
print_summary() {
    echo ""
    log_success "Bootstrap complete! Here's what was created:"
    echo ""
    echo "  IAM User:        ${PROJECT_NAME}-assistant"
    echo "  Secret Store:    ${PROJECT_NAME}/config (Secrets Manager)"
    echo "  S3 Bucket:       ${PROJECT_NAME}-backups-${ACCOUNT_ID}"
    echo "  Region:          $AWS_REGION"
    echo "  Budget Alert:    \$${BUDGET_AMOUNT}/month (manual setup required)"
    echo ""
    log_info "Next steps:"
    echo "  1. Save the access key credentials shown above"
    echo "  2. Configure your AI assistant to use these AWS resources"
    echo "  3. Store API keys in Secrets Manager: aws secretsmanager put-secret-value --secret-id ${PROJECT_NAME}/config"
    echo "  4. Set up budget alerts manually: https://console.aws.amazon.com/billing/home#/budgets"
    echo "  5. Test S3 backup: ./s3/vault-backup.sh /path/to/vault s3://${PROJECT_NAME}-backups-${ACCOUNT_ID}"
    echo ""
}

# Main execution
main() {
    echo ""
    log_info "AWS Infrastructure Bootstrap for $PROJECT_NAME"
    echo ""

    if [ "$DRY_RUN" = "true" ]; then
        log_warning "Running in DRY RUN mode - no resources will be created"
        echo ""
    fi

    check_prerequisites
    echo ""

    create_iam_user
    echo ""

    create_secrets_store
    echo ""

    create_s3_bucket
    echo ""

    setup_budget_alarm
    echo ""

    print_summary
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --project-name)
            PROJECT_NAME="$2"
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
        --budget)
            BUDGET_AMOUNT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: ./aws-bootstrap.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --dry-run              Run without creating resources"
            echo "  --project-name NAME    Project name (default: jarvis-ai)"
            echo "  --region REGION        AWS region (default: us-east-1)"
            echo "  --profile PROFILE      AWS CLI profile (default: default)"
            echo "  --budget AMOUNT        Monthly budget in USD (default: 10)"
            echo "  --help                 Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./aws-bootstrap.sh --dry-run"
            echo "  ./aws-bootstrap.sh --project-name my-ai --region us-west-2"
            echo "  ./aws-bootstrap.sh --profile personal --budget 20"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Run './aws-bootstrap.sh --help' for usage information"
            exit 1
            ;;
    esac
done

# Run main
main
