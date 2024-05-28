import os.path

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from models import UserModel
from schemas import UserSchema, UserUpdateSchema

blp = Blueprint("Users", __name__, description="Operations on users")


@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get(user_id)
        if user:
            user.fullname = user_data["fullname"]
            user.avatar = user_data["avatar"]
        else:
            user = UserModel(id=user_id, **user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while updating user.")
        return user

    @blp.response(200)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting user.")
        return {"message": "User successfully deleted."}


@blp.route("/users/<string:company_id>")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self, company_id):
        return UserModel.query.filter_by(company_id=company_id)

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data, company_id):
        user = UserModel(**user_data, company_id=company_id)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Username is already existed.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while registering user.")

        # create user directory
        user_dir = os.path.join(os.path.dirname(__file__), "..", "persons", user.company_id, user.username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        return user
