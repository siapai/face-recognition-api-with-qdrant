import uuid
from db import db
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(UNIQUEIDENTIFIER(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    fullname = db.Column(db.String(80), nullable=False)
    avatar = db.Column(db.String(200), nullable=True)

    company_id = db.Column(db.String(80), db.ForeignKey("companies.id"), unique=False, nullable=False)
    company = db.relationship("CompanyModel", back_populates="users")

    photos = db.relationship(
        "PhotoModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete"
    )

    recognitions = db.relationship(
        "RecognitionModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete"
    )

