function clear_s3_bucket ()
{
    aws s3 rm core-framework-bucket --recursive --exclude="*" --include="*.tar.gz"
}

clear_s3_bucket