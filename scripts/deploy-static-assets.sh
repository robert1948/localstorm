#!/usr/bin/env bash
set -e

# === Directory structure relative to client ===
STATIC_DIR="public/static"
IMG_DIR="$STATIC_DIR/img"
MANIFEST_DIR="$STATIC_DIR/manifest"
ICONS_DIR="$IMG_DIR/icons"
S3_BUCKET="s3://lightning-s3/static/website/img"

# === Upload static manifest ===
echo "🚀 Uploading static manifest..."
if [ -f "$MANIFEST_DIR/site.webmanifest" ]; then
  aws s3 cp "$MANIFEST_DIR/site.webmanifest" "$S3_BUCKET/site.webmanifest" \
    --content-type "application/manifest+json"
else
  echo "⚠️ Skipped: $MANIFEST_DIR/site.webmanifest not found."
fi

# === Upload dashboard preview ===
echo "📸 Uploading dashboard preview..."
DASHBOARD="$IMG_DIR/dashboard-preview.png"
if [ -f "$DASHBOARD" ]; then
  aws s3 cp "$DASHBOARD" "$S3_BUCKET/dashboard-preview.png"
else
  echo "⚠️ Skipped: $DASHBOARD not found."
fi

# === Upload logo variants ===
echo "🎯 Uploading logo variants..."
LOGO="$IMG_DIR/logo-64x64.png"
if [ -f "$LOGO" ]; then
  echo "📤 $LOGO ➜ $S3_BUCKET/logo-64x64.png"
  aws s3 cp "$LOGO" "$S3_BUCKET/logo-64x64.png"
else
  echo "⚠️ Skipped: $LOGO not found."
fi

# === Upload favicons and icons ===
echo "🌟 Uploading favicons and icons..."
for icon in apple-touch-icon.png favicon-32x32.png favicon-16x16.png; do
  ICON_PATH="$ICONS_DIR/$icon"
  if [ -f "$ICON_PATH" ]; then
    echo "📤 $ICON_PATH ➜ $S3_BUCKET/icons/$icon"
    aws s3 cp "$ICON_PATH" "$S3_BUCKET/icons/$icon" --content-type "image/png"
  else
    echo "⚠️ Skipped: $ICON_PATH not found."
  fi
done

echo "✅ All static image assets uploaded with correct headers."

