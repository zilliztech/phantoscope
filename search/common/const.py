OPERATOR_TYPE_ENCODER = "encoder"
OPERATOR_TYPE_PROCESSOR = "processor"

MINIO_BUCKET_PUBLIC_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": ["s3:GetObject", "s3:GetBucketLocation"],
            "Effect": "Allow",
            "Resource": ["arn:aws:s3:::ad/*", "arn:aws:s3:::adaaa111"],
            "Principal": {"AWS": "*"},
            "Sid": "Public"
        }
    ]
}
