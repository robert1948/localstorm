# Manual AWS S3 Public Access Setup Guide

## Step-by-Step AWS Console Instructions

### Prerequisites
- Access to AWS Console
- Permissions to modify S3 bucket settings
- Your S3 bucket: `lightning-s3`

---

## Step 1: Access Your S3 Bucket

1. **Log into AWS Console**: https://console.aws.amazon.com
2. **Navigate to S3**: Services → Storage → S3
3. **Find your bucket**: Click on `lightning-s3`

---

## Step 2: Remove Public Access Blocks

1. **Go to Permissions tab** in your bucket
2. **Find "Block public access (bucket settings)"**
3. **Click "Edit"**
4. **Uncheck ALL four boxes:**
   - [ ] Block public access to buckets and objects granted through new access control lists (ACLs)
   - [ ] Block public access to buckets and objects granted through any access control lists (ACLs)
   - [ ] Block public access to buckets and objects granted through new public bucket or access point policies
   - [ ] Block public access to buckets and objects granted through any public bucket or access point policies
5. **Click "Save changes"**
6. **Type "confirm" in the confirmation box**
7. **Click "Confirm"**

**⚠️ Warning:** AWS will show a warning about making your bucket public. This is expected.

---

## Step 3: Apply Bucket Policy

1. **Still in Permissions tab**
2. **Find "Bucket policy" section**
3. **Click "Edit"**
4. **Copy and paste this policy** (replace if there's existing content):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::lightning-s3/static/website/img/*"
        }
    ]
}
```

5. **Click "Save changes"**

**✅ This policy allows public read access to all files in the `static/website/img/` folder.**

---

## Step 4: Make Existing Files Public

### Option A: Make All Files Public (Recommended)

1. **Go to Objects tab**
2. **Navigate to folder**: `static/website/img/`
3. **Select all files** (check the box next to "Name" to select all)
4. **Click "Actions" dropdown**
5. **Select "Make public using ACL"**
6. **Click "Make public"**

### Option B: Make Individual Files Public

1. **Go to Objects tab**
2. **Navigate to**: `static/website/img/`
3. **Click on a specific file** (e.g., `landing01.png`)
4. **Go to Permissions tab**
5. **Under "Access control list (ACL)"**
6. **Click "Edit"**
7. **Under "Everyone (public access)":**
   - Check "Read" checkbox
8. **Click "Save changes"**
9. **Repeat for each file you want to make public**

---

## Step 5: Verify Public Access

### Test URLs in Browser:
```
https://lightning-s3.s3.amazonaws.com/static/website/img/landing01.png
https://lightning-s3.s3.amazonaws.com/static/website/img/capecontrol-logo.png
https://lightning-s3.s3.amazonaws.com/static/website/img/logo-64x64.png
```

### Each URL should:
- ✅ Load the image directly
- ✅ Not show any error or access denied message
- ✅ Display the file content

---

## Step 6: Update Your React Components

Once files are publicly accessible, update your components:

### In `client/src/components/Hero.jsx`:
```jsx
// Change from:
src="/static/landing01.png"

// To:
src="https://lightning-s3.s3.amazonaws.com/static/website/img/landing01.png"
```

### In `client/src/components/Navbar.jsx`:
```jsx
// This should already be correct:
src="https://lightning-s3.s3.amazonaws.com/static/website/img/capecontrol-logo.png"
```

---

## Troubleshooting

### If you still get 403 errors:

1. **Check bucket policy syntax** - Copy it exactly from above
2. **Verify ACL permissions** - Make sure "Read" is checked for "Everyone"
3. **Wait 5-10 minutes** - DNS propagation can take time
4. **Check file path** - Ensure files are in `static/website/img/` folder
5. **Try incognito/private browsing** - Avoid browser cache issues

### Common Issues:

**❌ 403 Forbidden:**
- Bucket policy not applied correctly
- Files don't have public ACL
- Block public access still enabled

**❌ 404 Not Found:**
- Wrong file path
- File doesn't exist in the specified location

**❌ Policy Error:**
- JSON syntax error in bucket policy
- Incorrect bucket name in policy

---

## Security Considerations

**✅ What this setup does:**
- Makes only the `static/website/img/` folder public
- Keeps other bucket contents private
- Allows read-only access (no uploads/modifications)

**⚠️ Be aware:**
- These files will be publicly accessible to anyone
- Consider using CloudFront for better performance
- Monitor your AWS billing for data transfer costs

---

## Alternative: Upload New Files with Public Access

If you need to upload new files that are automatically public:

1. **Go to Objects tab**
2. **Click "Upload"**
3. **Add files**
4. **Expand "Permissions"**
5. **Under "Predefined ACLs"**
6. **Select "Grant public-read access"**
7. **Click "Upload"**

---

## Next Steps

After completing this setup:

1. **Test all image URLs** in your browser
2. **Update React components** to use S3 URLs
3. **Deploy your changes**
4. **Monitor performance** and consider CloudFront for production

**🎉 Your S3 files should now be publicly accessible!**
