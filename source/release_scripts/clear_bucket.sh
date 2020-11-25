function clear_s3_bucket ()
{
    aws s3 rm arn:aws:s3:eu-central-1::core-framework-bucket --recursive --exclude="*" --include="*.tar.gz"
}

clear_s3_bucket