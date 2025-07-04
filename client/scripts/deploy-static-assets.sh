#!/bin/bash

set -e

echo "📦 Building frontend assets..."
npm run build

echo "🚀 Uploading static assets to S3 with correct Content-Type headers..."

UPLOAD_DIR="dist/assets"
S3_BUCKET="s3://lightning-s3/static/website/img"

# Upload common image types with headers
find "$UPLOAD_DIR" \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.svg" -o -iname "*.webp" -o -iname "*.ico" \) | while read -r file; do
  filename=$(basename "$file")
  extension="${filename##*.}"

  case "$extension" in
    png)  content_type="image/png" ;;
    jpg|jpeg) content_type="image/jpeg" ;;
    svg)  content_type="image/svg+xml" ;;
    webp) content_type="image/webp" ;;
    ico)  content_type="image/x-icon" ;;
    *)    content_type="application/octet-stream" ;;
  esac

  echo "→ Uploading $filename with Content-Type: $content_type"
  aws s3 cp "$file" "$S3_BUCKET/$filename" --content-type "$content_type"
done

echo "✅ Upload complete!"
