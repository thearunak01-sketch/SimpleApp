from datetime import datetime, timezone

from app.extensions import db


class Image(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(512), nullable=False, unique=True)
    file_size = db.Column(db.BigInteger, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = db.relationship("User", back_populates="images")

    def to_dict(self, view_url=None):
        return {
            "id": self.id,
            "original_filename": self.original_filename,
            "stored_filename": self.stored_filename,
            "file_size": self.file_size,
            "width": self.width,
            "height": self.height,
            "created_at": self.created_at.isoformat(),
            "view_url": view_url,
        }
