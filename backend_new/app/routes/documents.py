from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.document import Document
from app.services.file_service import remove_uploaded_file, store_document
from app.services.storage_service import create_download_url
from app.utils.errors import StorageError, ValidationError
from app.utils.pagination import pagination_response, parse_pagination_args

documents_bp = Blueprint("documents", __name__)


def _owner_id():
    return int(get_jwt_identity())


def _upload_one(file, user_id):
    uploaded = store_document(file, user_id)
    try:
        db.session.add(uploaded["record"])
        db.session.commit()
        return uploaded["record"]
    except Exception:
        db.session.rollback()
        remove_uploaded_file(uploaded["key"])
        raise


@documents_bp.post("/upload")
@jwt_required()
def upload_document():
    try:
        document = _upload_one(request.files.get("file"), _owner_id())
    except (ValidationError, StorageError) as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"item": document.to_dict(), "message": "Document uploaded."}), 201


@documents_bp.post("/upload-multiple")
@jwt_required()
def upload_multiple_documents():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "Select at least one document."}), 400

    items = []
    errors = []
    for file in files:
        try:
            items.append(_upload_one(file, _owner_id()).to_dict())
        except (ValidationError, StorageError) as error:
            errors.append({"filename": file.filename or "unnamed file", "error": str(error)})
    status = 201 if items else 400
    return jsonify({"items": items, "errors": errors, "message": f"Uploaded {len(items)} document(s)."}), status


@documents_bp.get("")
@jwt_required()
def list_documents():
    try:
        page, per_page = parse_pagination_args(request, 10)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    pagination = Document.query.filter_by(user_id=_owner_id()).order_by(Document.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(pagination_response(pagination, lambda item: item.to_dict()))


@documents_bp.get("/<int:document_id>/download")
@jwt_required()
def download_document(document_id):
    document = Document.query.filter_by(id=document_id, user_id=_owner_id()).first()
    if not document:
        return jsonify({"error": "Document not found."}), 404
    try:
        url = create_download_url(document.s3_key, document.original_filename, download=True)
    except StorageError as error:
        return jsonify({"error": str(error)}), 503
    return jsonify({"download_url": url})
