from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import db
from app.models.user import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.get("/profile")
@jwt_required()
def profile():
    user = db.session.get(User, int(get_jwt_identity()))
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()})
