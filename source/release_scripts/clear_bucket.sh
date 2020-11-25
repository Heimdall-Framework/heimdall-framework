function clear_s3_bucket ()
{
    aws s3 rm s3://core-framework-bucket --recursive --exclude="*" --include="*.tar.gz"
}

clear_s3_bucket