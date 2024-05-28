import os.path

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import CompanyModel
from schemas import CompanySchema

blp = Blueprint("Companies", __name__, description="Operations on companies")


@blp.route("/company/<string:company_id>")
class Company(MethodView):
    @blp.response(200, CompanySchema)
    def get(self, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        return company

    @blp.response(200)
    def delete(self, company_id):
        company = CompanyModel.query.get_or_404(company_id)
        try:
            db.session.delete(company)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting company.")
        return {"message": "Company successfully deleted."}


@blp.route("/company")
class CompanyList(MethodView):
    @blp.response(200, CompanySchema(many=True))
    def get(self):
        return CompanyModel.query.all()

    @blp.arguments(CompanySchema)
    @blp.response(201, CompanySchema)
    def post(self, company_data):
        company = CompanyModel(**company_data)
        try:
            db.session.add(company)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Company is already existed.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while registering company.")

        # create company directory
        company_dir = os.path.join(os.path.dirname(__file__), "..", "persons", company.id.upper())
        if not os.path.exists(company_dir):
            os.makedirs(company_dir)

        return company
