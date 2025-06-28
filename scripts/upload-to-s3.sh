#!/bin/bash
set -e

echo "🔁 Uploading static assets to S3..."

aws s3 sync client/public/ s3://lightning-s3/static/website/img/ --delete

echo "✅ Upload complete: https://lightning-s3.s3.amazonaws.com/static/website/img/"
