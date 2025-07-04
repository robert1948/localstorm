#!/bin/bash

echo "🚀 Uploading website images to S3..."

aws s3 cp client/public/static/capecontrol-logo.png s3://lightning-s3/static/website/img/capecontrol-ss.png
aws s3 cp client/public/static/logo-192x192.png     s3://lightning-s3/static/website/img/logo-192x192.png
aws s3 cp client/public/static/logo-128x128.png     s3://lightning-s3/static/website/img/logo-128x128.png
aws s3 cp client/public/static/logo-512x512.png     s3://lightning-s3/static/website/img/logo-512x512.png
aws s3 cp client/public/static/logo-64x64.png       s3://lightning-s3/static/website/img/logo-64x64.png

echo "✅ Upload complete!"
