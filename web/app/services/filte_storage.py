from botocore.exceptions import ClientError
from aiobotocore.session import AioBaseClient

from app.core.config import Config
from app.services.abstracts import AbstractFilesStorage


class FileDoesNotExist(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class S3FilesStorage(AbstractFilesStorage):
    def __init__(self, client: AioBaseClient, config: Config):
        self.client = client
        self.config = config

    async def put_file(self, file_name: str, content: bytes):
        """"""

        key = f"media/{file_name}"

        await self.client.put_object(
            Bucket=self.config.s3_bucket_name,
            Key=key,
            Body=content,
        )

    async def get_file(self, file_name: str) -> bytes:
        """"""

        key = f"media/{file_name}"

        try:
            response = await self.client.get_object(
                Bucket=self.config.s3_bucket_name, Key=key
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileDoesNotExist(
                    message=f"File with name={file_name} does not exist"
                )
            else:
                raise

        # this will ensure the connection is correctly re-used/closed
        async with response["Body"] as stream:
            data = await stream.read()

        return data

    async def get_file_stream(self, file_name: str):
        """"""

        key = f"media/{file_name}"

        try:
            response = await self.client.get_object(
                Bucket=self.config.s3_bucket_name, Key=key
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                raise FileDoesNotExist(
                    message=f"File with name={file_name} does not exist"
                )
            else:
                raise

        async with response["Body"] as stream:
            chunk: bytes = await stream.read()
            yield chunk

    async def delete_file(self, file_name: str):
        """"""

        key = f"media/{file_name}"

        await self.client.delete_object(Bucket=self.config.s3_bucket_name, Key=key)
