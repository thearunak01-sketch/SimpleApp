from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, set_access_cookies, unset_jwt_cookies

from app.models.user import User
from app.services.auth_service import register_user
from app.utils.errors import ValidationError

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    try:
        user = register_user(request.get_json(silent=True) or {})
    except ValidationError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify({"user": user.to_dict(), "message": "Account created."}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    token = create_access_token(identity=str(user.id))
    response = jsonify({"user": user.to_dict(), "message": "Signed in."})
    set_access_cookies(response, token)
    return response


@auth_bp.post("/logout")
@jwt_required()
def logout():
    response = jsonify({"message": "Signed out."})
    unset_jwt_cookies(response)
    return response


@auth_bp.get("/session")
@jwt_required()
def session():
    user = User.query.get(int(get_jwt()["sub"]))
    if not user:
        return jsonify({"error": "User not found."}), 401
    return jsonify({"user": user.to_dict()})
