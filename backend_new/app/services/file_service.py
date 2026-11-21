from io import BytesIO
from pathlib import Path
from uuid import uuid4

from flask import current_app
from PIL import Image as PillowImage
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.models.document import Document
from app.models.image import Image
from app.services.storage_service import delete_object, upload_bytes
from app.utils.errors import ValidationError

IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
IMAGE_FORMATS = {"JPEG", "PNG", "WEBP", "GIF"}
DOCUMENT_MIME_TYPES = {
    "pdf": {"application/pdf"},
    "txt": {"text/plain", "application/octet-stream"},
    "doc": {"application/msword", "application/octet-stream"},
    "docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/octet-stream"},
}


def _required_file(file, label):
    if not file or not file.filename:
        raise ValidationError(f"{label} is required.")
    return file


def process_image(file: FileStorage, user_id):
    _required_file(file, "An image file")
    if file.mimetype not in IMAGE_MIME_TYPES:
        raise ValidationError("Use JPEG, PNG, WebP, or GIF images only.")

    raw = file.read()
    if len(raw) > current_app.config["IMAGE_MAX_BYTES"]:
        raise ValidationError("Images must be 5 MB or smaller.")

    try:
        source_file = PillowImage.open(BytesIO(raw))
        detected_format = source_file.format
        source_file.verify()
        source = PillowImage.open(BytesIO(raw)).convert("RGB")
    except Exception as error:
        raise ValidationError("The uploaded file is not a valid image.") from error

    if detected_format not in IMAGE_FORMATS:
        raise ValidationError("The image format is not supported.")

    source.thumbnail((current_app.config["MAX_IMAGE_DIMENSION"], current_app.config["MAX_IMAGE_DIMENSION"]), PillowImage.Resampling.LANCZOS)
    output = BytesIO()
    source.save(output, format="WEBP", quality=85, method=6)
    output.seek(0)

    stored_filename = f"{uuid4().hex}.webp"
    key = f"images/{user_id}/{stored_filename}"
    upload_bytes(output, key, "image/webp")
    return {
        "record": Image(
            user_id=user_id,
            original_filename=secure_filename(file.filename) or "image",
            stored_filename=stored_filename,
            s3_key=key,
            file_size=output.getbuffer().nbytes,
            width=source.width,
            height=source.height,
        ),
        "key": key,
    }


def store_document(file: FileStorage, user_id):
    _required_file(file, "A document file")
    original_name = secure_filename(file.filename)
    extension = Path(original_name).suffix.lower().lstrip(".") if original_name else ""
    if extension not in DOCUMENT_MIME_TYPES:
        raise ValidationError("Only PDF, TXT, DOC, and DOCX files are allowed.")
    if file.mimetype and file.mimetype not in DOCUMENT_MIME_TYPES[extension]:
        raise ValidationError("The file type does not match its extension.")

    raw = file.read()
    if len(raw) > current_app.config["DOCUMENT_MAX_BYTES"]:
        raise ValidationError("Documents must be 10 MB or smaller.")

    stored_filename = f"{uuid4().hex}.{extension}"
    key = f"documents/{user_id}/{stored_filename}"
    upload_bytes(BytesIO(raw), key, file.mimetype or "application/octet-stream")
    return {
        "record": Document(
            user_id=user_id,
            original_filename=original_name or f"document.{extension}",
            stored_filename=stored_filename,
            s3_key=key,
            file_type=extension,
            file_size=len(raw),
        ),
        "key": key,
    }


def remove_uploaded_file(key):
    delete_object(key)
