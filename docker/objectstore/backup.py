import asyncio
import os
import sys
from aiobotocore.session import get_session

OBJECT_STORE_KEY = os.environ["OBJECT_STORE_KEY"]
OBJECT_STORE_SECRET = os.environ["OBJECT_STORE_SECRET"]
OBJECT_STORE_HOST = os.environ["OBJECT_STORE_HOST"]
OBJECT_STORE_BUCKET = os.environ["OBJECT_STORE_BUCKET"]

async def go():
    filename = sys.argv[1]

    session = get_session()
    async with session.create_client('s3',
            endpoint_url=f'https://{OBJECT_STORE_HOST}',
            aws_secret_access_key=OBJECT_STORE_SECRET,
            aws_access_key_id=OBJECT_STORE_KEY) as client:
        # upload object to amazon s3
        data = b'\x01' * 1024
        resp = await client.put_object(Bucket=OBJECT_STORE_BUCKET,
                                       Key=filename,
                                       Body=data)
        print(resp)

        # getting s3 object properties of file we just uploaded
        resp = await client.get_object_acl(Bucket=OBJECT_STORE_BUCKET, Key=filename)
        print(resp)

        # delete object from s3
        resp = await client.delete_object(Bucket=OBJECT_STORE_BUCKET, Key=filename)
        print(resp)


if __name__ == '__main__':
    asyncio.run(go())