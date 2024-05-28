import uuid
from db import db
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import func


class RecognitionModel(db.Model):
    __tablename__ = "recognitions"

    id = db.Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="recognitions")

    photo_id = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("photos.id"), unique=False, nullable=False)
    photo = db.relationship("PhotoModel",  foreign_keys=[photo_id])

    matched_photo_id = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("photos.id"), unique=False, nullable=True)
    matched_photo = db.relationship("PhotoModel", foreign_keys=[matched_photo_id])
    matched_score = db.Column(db.Float())

    logged_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

