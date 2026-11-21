import boto3
from botocore.exceptions import BotoCoreError, ClientError
from flask import current_app

from app.utils.errors import StorageError


def _client():
    return boto3.client(
        "s3",
        region_name=current_app.config["AWS_REGION"],
        aws_access_key_id=current_app.config.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=current_app.config.get("AWS_SECRET_ACCESS_KEY"),
    )


def upload_bytes(content, key, content_type):
    try:
        _client().put_object(
            Bucket=current_app.config["S3_BUCKET_NAME"],
            Key=key,
            Body=content,
            ContentType=content_type,
        )
    except (BotoCoreError, ClientError) as error:
        raise StorageError("File storage is unavailable.") from error


def delete_object(key):
    try:
        _client().delete_object(Bucket=current_app.config["S3_BUCKET_NAME"], Key=key)
    except (BotoCoreError, ClientError) as error:
        raise StorageError("File storage is unavailable.") from error


def create_download_url(key, filename=None, download=False):
    params = {"Bucket": current_app.config["S3_BUCKET_NAME"], "Key": key}
    if filename:
        disposition = "attachment" if download else "inline"
        safe_filename = filename.replace('"', "")
        params["ResponseContentDisposition"] = f'{disposition}; filename="{safe_filename}"'
    try:
        return _client().generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=current_app.config["PRESIGNED_URL_EXPIRY"],
        )
    except (BotoCoreError, ClientError) as error:
        raise StorageError("File storage is unavailable.") from error
