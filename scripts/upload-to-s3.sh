#!/bin/bash

# Exit on any error
set -e

# S3 bucket and path (adjust if needed)
BUCKET_NAME=lightning-s3
REGION=us-east-1
DEST_PATH=static/website/img/

# Directory to upload
SOURCE_DIR=dist/assets/

# Sync to S3
echo "📤 Uploading $SOURCE_DIR to s3://$BUCKET_NAME/$DEST_PATH"
aws s3 sync "$SOURCE_DIR" "s3://$BUCKET_NAME/$DEST_PATH" --region "$REGION" --delete

echo "✅ Upload complete."
