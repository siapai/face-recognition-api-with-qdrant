from db import db


class CompanyModel(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.String(80), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    address = db.Column(db.String(256), nullable=True)

    users = db.relationship(
        "UserModel",
        back_populates="company",
        lazy="dynamic",
        cascade="all, delete"
    )

