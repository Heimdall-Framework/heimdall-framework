function clear_s3_bucket ()
{
    aws s3 rm s3://premium-plugins-bucket --recursive --exclude="*" --include="*-$OLD_VERSION"
}

clear_s3_bucket