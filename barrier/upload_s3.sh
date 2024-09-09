#!/bin/bash
# Define variables
BUCKET_NAME=""
PHOTO_PATH=$1
TIMESTAMP=$(date +%Y%m%d%H%M%S)
UPLOAD_PATH="images/$TIMESTAMP.jpg"

# Upload the photo to S3
aws s3 cp $PHOTO_PATH s3://$BUCKET_NAME/$UPLOAD_PATH
echo "Photo uploaded to s3://$BUCKET_NAME/$UPLOAD_PATH"