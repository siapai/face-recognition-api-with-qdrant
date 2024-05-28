import uuid
from db import db
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy import func
from sqlalchemy.sql import expression


class PhotoModel(db.Model):
    __tablename__ = "photos"

    id = db.Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = db.Column(db.String(256), unique=True, nullable=False)
    dir_path = db.Column(db.String(256), nullable=False)
    url_path = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    face_model = db.Column(db.Boolean, server_default=expression.false(),  nullable=False)
    face_recognition = db.Column(db.Boolean, server_default=expression.false(), nullable=False)

    user_id = db.Column(UNIQUEIDENTIFIER, db.ForeignKey("users.id"), unique=False, nullable=False)
    user = db.relationship("UserModel", back_populates="photos")
