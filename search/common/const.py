# Copyright (C) 2019-2020 Zilliz. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing permissions and limitations under the License.


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

MARKET_IDENTITY_HEADER = "phantoscope_market_version"

INSTANCE_STATUS_RUNNING = "running"
