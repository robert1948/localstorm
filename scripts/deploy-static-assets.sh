#!/usr/bin/env bash
set -e

# === Directory structure relative to client ===
STATIC_DIR="public/static"
MANIFEST_FILE="public/static/manifest/site.webmanifest"
S3_BUCKET="s3://lightning-s3/static/website/img"

# === Upload static manifest ===
echo "🚀 Uploading static manifest..."
if [ -f "$MANIFEST_FILE" ]; then
  aws s3 cp "$MANIFEST_FILE" "$S3_BUCKET/site.webmanifest" \
    --content-type "application/manifest+json"
else
  echo "⚠️ Skipped: $MANIFEST_FILE not found."
fi

# === Upload dashboard preview ===
echo "📸 Uploading dashboard preview..."
DASHBOARD="$STATIC_DIR/dashboard-preview.png"
if [ -f "$DASHBOARD" ]; then
  aws s3 cp "$DASHBOARD" "$S3_BUCKET/dashboard-preview.png" --content-type "image/png"
else
  echo "⚠️ Skipped: $DASHBOARD not found."
fi

# === Upload main logo ===
echo "🏷️ Uploading main logo..."
MAIN_LOGO="$STATIC_DIR/capecontrol-logo.png"
if [ -f "$MAIN_LOGO" ]; then
  aws s3 cp "$MAIN_LOGO" "$S3_BUCKET/capecontrol-logo.png" --content-type "image/png"
  echo "📤 $MAIN_LOGO ➜ $S3_BUCKET/capecontrol-logo.png"
else
  echo "⚠️ Skipped: $MAIN_LOGO not found."
fi

# === Upload logo variants ===
echo "🎯 Uploading logo variants..."
for size in 64 128 192 512; do
  LOGO="$STATIC_DIR/logo-${size}x${size}.png"
  if [ -f "$LOGO" ]; then
    echo "📤 $LOGO ➜ $S3_BUCKET/logo-${size}x${size}.png"
    aws s3 cp "$LOGO" "$S3_BUCKET/logo-${size}x${size}.png" --content-type "image/png"
  else
    echo "⚠️ Skipped: $LOGO not found."
  fi
done

# === Upload favicons and icons ===
echo "🌟 Uploading favicons and icons..."
for icon in apple-touch-icon.png favicon-32x32.png favicon-16x16.png; do
  ICON_PATH="$STATIC_DIR/$icon"
  if [ -f "$ICON_PATH" ]; then
    echo "📤 $ICON_PATH ➜ $S3_BUCKET/$icon"
    aws s3 cp "$ICON_PATH" "$S3_BUCKET/$icon" --content-type "image/png"
  else
    echo "⚠️ Skipped: $ICON_PATH not found."
  fi
done

echo "✅ All static image assets uploaded with correct headers."

