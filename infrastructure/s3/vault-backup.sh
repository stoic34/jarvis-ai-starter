#!/usr/bin/env bash

set -e

# Vault Backup to S3
# Syncs your Obsidian vault to an S3 bucket for safe, versioned backups

# Usage:
#   ./vault-backup.sh /path/to/vault s3://bucket-name
#   ./vault-backup.sh /path/to/vault s3://bucket-name --dry-run
#   ./vault-backup.sh /path/to/vault s3://bucket-name --prefix backups/vault

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
Vault Backup to S3

Usage:
  $0 VAULT_PATH S3_BUCKET [OPTIONS]

Arguments:
  VAULT_PATH    Path to your Obsidian vault directory
  S3_BUCKET     S3 bucket URL (e.g., s3://my-backups)

Options:
  --dry-run           Show what would be synced without actually syncing
  --prefix PREFIX     S3 key prefix (default: vault-backups)
  --profile PROFILE   AWS CLI profile to use
  --region REGION     AWS region (default: us-east-1)
  --help              Show this help message

Examples:
  # Basic backup
  $0 ~/Documents/MyVault s3://my-backup-bucket

  # Dry run to see what would be synced
  $0 ~/Documents/MyVault s3://my-backup-bucket --dry-run

  # Backup to specific prefix
  $0 ~/Documents/MyVault s3://my-backup-bucket --prefix backups/vault

  # Use specific AWS profile
  $0 ~/Documents/MyVault s3://my-backup-bucket --profile personal

Excluded from backup:
  - .git/                (Git repository)
  - .obsidian/plugins/   (Obsidian plugins - can be reinstalled)
  - node_modules/        (Dependencies - can be reinstalled)
  - .DS_Store            (macOS metadata)
  - .trash/              (Obsidian trash)

IMPORTANT: This script uses 'aws s3 sync' WITHOUT --delete flag.
Files deleted from your vault will NOT be deleted from S3.
This provides protection against accidental deletions.

EOF
}

# Parse arguments
VAULT_PATH=""
S3_BUCKET=""
DRY_RUN=""
S3_PREFIX="vault-backups"
AWS_PROFILE=""
AWS_REGION="us-east-1"

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN="--dryrun"
            shift
            ;;
        --prefix)
            S3_PREFIX="$2"
            shift 2
            ;;
        --profile)
            AWS_PROFILE="$2"
            shift 2
            ;;
        --region)
            AWS_REGION="$2"
            shift 2
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
            if [ -z "$VAULT_PATH" ]; then
                VAULT_PATH="$1"
            elif [ -z "$S3_BUCKET" ]; then
                S3_BUCKET="$1"
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
if [ -z "$VAULT_PATH" ] || [ -z "$S3_BUCKET" ]; then
    log_error "Missing required arguments"
    echo ""
    show_usage
    exit 1
fi

# Validate vault path exists
if [ ! -d "$VAULT_PATH" ]; then
    log_error "Vault path does not exist: $VAULT_PATH"
    exit 1
fi

# Validate S3 bucket format
if [[ ! "$S3_BUCKET" =~ ^s3:// ]]; then
    log_error "S3 bucket must start with 's3://'"
    exit 1
fi

# Check AWS CLI is installed
if ! command -v aws &> /dev/null; then
    log_error "AWS CLI is not installed. Install from: https://aws.amazon.com/cli/"
    exit 1
fi

# Check AWS credentials
PROFILE_ARG=""
if [ -n "$AWS_PROFILE" ]; then
    PROFILE_ARG="--profile $AWS_PROFILE"
fi

if ! aws sts get-caller-identity $PROFILE_ARG &> /dev/null; then
    log_error "AWS credentials not configured. Run: aws configure"
    exit 1
fi

# Build S3 destination URL
S3_DESTINATION="${S3_BUCKET%/}/${S3_PREFIX}"

# Generate timestamp for tagging
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Display backup info
echo ""
log_info "Vault Backup to S3"
echo ""
echo "  Vault:       $VAULT_PATH"
echo "  Destination: $S3_DESTINATION"
echo "  Region:      $AWS_REGION"
if [ -n "$AWS_PROFILE" ]; then
    echo "  Profile:     $AWS_PROFILE"
fi
if [ -n "$DRY_RUN" ]; then
    log_warning "DRY RUN MODE - No files will be synced"
fi
echo ""

# Build AWS sync command with exclusions
SYNC_CMD="aws s3 sync"
SYNC_CMD="$SYNC_CMD \"$VAULT_PATH\""
SYNC_CMD="$SYNC_CMD \"$S3_DESTINATION\""

# Add exclusions (CRITICAL: no --delete flag to preserve deleted files in S3)
SYNC_CMD="$SYNC_CMD --exclude .git/"
SYNC_CMD="$SYNC_CMD --exclude .git/*"
SYNC_CMD="$SYNC_CMD --exclude .obsidian/plugins/*"
SYNC_CMD="$SYNC_CMD --exclude node_modules/"
SYNC_CMD="$SYNC_CMD --exclude node_modules/*"
SYNC_CMD="$SYNC_CMD --exclude .DS_Store"
SYNC_CMD="$SYNC_CMD --exclude .trash/"
SYNC_CMD="$SYNC_CMD --exclude .trash/*"
SYNC_CMD="$SYNC_CMD --exclude '*.tmp'"

# Add metadata tags
SYNC_CMD="$SYNC_CMD --metadata backup-timestamp=$TIMESTAMP"

# Add optional flags
if [ -n "$DRY_RUN" ]; then
    SYNC_CMD="$SYNC_CMD $DRY_RUN"
fi

if [ -n "$AWS_PROFILE" ]; then
    SYNC_CMD="$SYNC_CMD --profile $AWS_PROFILE"
fi

if [ -n "$AWS_REGION" ]; then
    SYNC_CMD="$SYNC_CMD --region $AWS_REGION"
fi

# Execute sync
log_info "Starting sync..."
echo ""

# Run the sync command (eval to handle quoted paths properly)
eval $SYNC_CMD

echo ""

# Show results
if [ -n "$DRY_RUN" ]; then
    log_success "Dry run complete - no files were synced"
else
    log_success "Backup complete!"
    log_info "Your vault has been backed up to: $S3_DESTINATION"
    log_info "Backup timestamp: $TIMESTAMP"
    echo ""
    log_info "To restore from backup:"
    echo "  aws s3 sync $S3_DESTINATION /path/to/restore/location"
    echo ""
    log_info "To view backup contents:"
    echo "  aws s3 ls $S3_DESTINATION/ --recursive"
fi

echo ""

# IMPORTANT: Remind about --delete flag
if [ -z "$DRY_RUN" ]; then
    log_warning "Note: This backup uses 'aws s3 sync' WITHOUT --delete flag"
    log_warning "Files deleted from your vault are preserved in S3 for safety"
    echo ""
fi

exit 0
