# PNG Image Preservation Guide

## Overview
This document ensures all PNG images in the LocalStorm project are properly preserved and uploaded to S3 CDN without being accidentally deleted.

## Key Files Modified

### 1. Upload Script Enhancement
**File:** `scripts/upload-to-s3.sh`
- **Removed:** `--delete` flag that could remove existing S3 files
- **Added:** Specific PNG image upload logic
- **Ensures:** All PNG files from `client/public/static/` are uploaded

### 2. PNG Preservation Script
**File:** `scripts/preserve-png-images.sh`
- **Purpose:** Comprehensive PNG backup to S3
- **Features:**
  - Uploads core branding images (LogoC.png, LogoW.png, capecontrol-logo.png)
  - Handles all PWA icons (16x16, 32x32, 192x192, 512x512)
  - Backs up landing page images
  - Searches entire project for additional PNG files
  - Sets proper content-type headers

### 3. PNG Verification Script
**File:** `scripts/verify-png-images.sh`
- **Purpose:** Verify all required PNG images exist in S3
- **Checks:** 13 critical PNG images needed for the application
- **Reports:** Missing images and provides remediation steps

### 4. Package.json Updates
**New Commands:**
- `npm run preserve:png` - Upload all PNG images to S3
- `npm run verify:png` - Verify PNG images are in S3
- Updated `heroku-postbuild` to include PNG preservation

## Required PNG Images

### Core Branding
- `LogoC.png` - Main colored logo
- `LogoW.png` - White logo for dark backgrounds
- `capecontrol-logo.png` - Full application logo

### Landing Page
- `landing01.png` - Hero section image

### PWA Icons
- `logo-64x64.png` - Small app icon
- `logo-128x128.png` - Medium app icon
- `logo-192x192.png` - Large app icon (PWA standard)
- `logo-512x512.png` - Extra large app icon (PWA standard)

### Favicons
- `favicon-16x16.png` - Browser tab icon (small)
- `favicon-32x32.png` - Browser tab icon (standard)

### Mobile/Platform Icons
- `apple-touch-icon.png` - iOS home screen icon
- `android-chrome-192x192.png` - Android app icon
- `android-chrome-512x512.png` - Android app icon (large)

## Usage Commands

### Deploy with PNG preservation:
```bash
npm run build
npm run preserve:png
```

### Verify PNG images are in S3:
```bash
npm run verify:png
```

### Heroku deployment (automatic):
```bash
# PNG preservation is now included in heroku-postbuild
git push heroku main
```

## S3 Location
All PNG images are stored at:
- **Bucket:** `lightning-s3`
- **Path:** `static/website/img/`
- **URL Base:** `https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/`

## Safety Measures

1. **No Delete Operations:** Upload scripts no longer use `--delete` flag
2. **Duplicate Checking:** Scripts check multiple source directories
3. **Verification:** Automated checking ensures all images are present
4. **Content-Type Headers:** Proper MIME types set for all PNG files
5. **Backup Sources:** Images backed up from both client and backend directories

## Troubleshooting

### If PNG images are missing:
1. Run `npm run verify:png` to identify missing images
2. Run `npm run preserve:png` to upload all PNG images
3. Check local directories for source files
4. Verify AWS credentials are configured

### If deployment fails:
1. Ensure AWS CLI is installed and configured
2. Check S3 bucket permissions
3. Verify all required PNG files exist locally
4. Run verification script to confirm uploads

## Project Impact
- **39 PNG files** total in project
- **13 critical images** for application functionality
- **Zero data loss** - all images preserved during deployments
- **CDN performance** - images served from S3 for faster loading
