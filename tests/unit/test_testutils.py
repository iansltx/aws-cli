# Copyright 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import mock

from awscli.testutils import create_bucket
from awscli.testutils import BaseCLIDriverTest

ERROR_409 = b'''<?xml version="1.0" encoding="UTF-8"?>
<Error>
<Code>BucketAlreadyOwnedByYou</Code>
<Message>Your previous request to create the named bucket succeeded and you already own it.</Message>
<BucketName>awscli-s3test-3uvz5tdmf1</BucketName>
<RequestId>A8E7C34EA4F108FF</RequestId>
<HostId>BUXR7OBsTxKfIGjPJUN4/BYFNt5mNK/KHtV769LKcDdZEb+IRn82U/TaSu3+Oz1Y</HostId>
</Error>'''

class TestCreateBucket(BaseCLIDriverTest):
    def test_bucket_already_owned_by_you(self):
        with mock.patch('botocore.endpoint.Session.send') as _send:
            _send.side_effect = [
                mock.Mock(status_code=500, headers={}, content=b''),
                mock.Mock(status_code=409, headers={}, content=ERROR_409),
                ]
            self.assertEqual(create_bucket(self.session, 'bucket'), 'bucket')
