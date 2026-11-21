from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.image import Image
from app.services.file_service import process_image, remove_uploaded_file
from app.services.storage_service import create_download_url
from app.utils.errors import StorageError, ValidationError
from app.utils.pagination import pagination_response, parse_pagination_args

images_bp = Blueprint("images", __name__)


def _owner_id():
    return int(get_jwt_identity())


def _serialize(image):
    return image.to_dict(create_download_url(image.s3_key, image.original_filename))


def _upload_one(file, user_id):
    uploaded = process_image(file, user_id)
    try:
        db.session.add(uploaded["record"])
        db.session.commit()
        return uploaded["record"]
    except Exception:
        db.session.rollback()
        remove_uploaded_file(uploaded["key"])
        raise


@images_bp.post("/upload")
@jwt_required()
def upload_image():
    try:
        image = _upload_one(request.files.get("file"), _owner_id())
    except (ValidationError, StorageError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"item": _serialize(image), "message": "Image uploaded."}), 201


@images_bp.post("/upload-multiple")
@jwt_required()
def upload_multiple_images():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "Select at least one image."}), 400

    items = []
    errors = []
    for file in files:
        try:
            items.append(_serialize(_upload_one(file, _owner_id())))
        except (ValidationError, StorageError) as error:
            errors.append({"filename": file.filename or "unnamed file", "error": str(error)})
    status = 201 if items else 400
    return jsonify({"items": items, "errors": errors, "message": f"Uploaded {len(items)} image(s)."}), status


@images_bp.get("")
@jwt_required()
def list_images():
    try:
        page, per_page = parse_pagination_args(request, 9)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    pagination = Image.query.filter_by(user_id=_owner_id()).order_by(Image.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(pagination_response(pagination, _serialize))
