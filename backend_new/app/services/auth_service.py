from email_validator import EmailNotValidError, validate_email

from app.extensions import db
from app.models.user import User
from app.utils.errors import ValidationError


def normalize_registration(data):
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    mobile = str(data.get("mobile", "")).strip()
    password = str(data.get("password", ""))

    if not name or len(name) > 120:
        raise ValidationError("Name is required and must be 120 characters or fewer.")
    if not mobile or len(mobile) > 32:
        raise ValidationError("Mobile number is required and must be 32 characters or fewer.")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters.")
    try:
        email = validate_email(email, check_deliverability=False).normalized
    except EmailNotValidError as error:
        raise ValidationError("Enter a valid email address.") from error
    return name, email, mobile, password


def register_user(data):
    name, email, mobile, password = normalize_registration(data)
    if User.query.filter_by(email=email).first():
        raise ValidationError("An account with that email already exists.")
    user = User(name=name, email=email, mobile=mobile)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
