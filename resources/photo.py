import os.path
from werkzeug.utils import secure_filename
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from insightface.app import FaceAnalysis

import face_recognition
from qdrant import client
from qdrant_client.http import models
from db import db
from models import PhotoModel, UserModel
from schemas import PhotoSchema, MultipartFileSchema, FormSchema

import numpy as np

blp = Blueprint(
    "Photos",
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), "..", "persons"),
    static_url_path='/static/person',
    description="Operations on photos"
)

registration = face_recognition.PersonRegistration()


@blp.route("/photo/<string:photo_id>")
class Photo(MethodView):
    @blp.response(200, PhotoSchema)
    def get(self, photo_id):
        photo = PhotoModel.query.get_or_404(photo_id)
        return photo

    @blp.response(200)
    def delete(self):
        photo = PhotoModel.query.get_or_404(photo_id)
        try:
            db.session.delete(photo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting photo.")
        return {"message": "Photo successfully deleted."}


@blp.route("/photos/<string:user_id>")
class PhotoList(MethodView):
    @blp.response(200, PhotoSchema(many=True))
    def get(self, user_id):
        return PhotoModel.query.filter_by(user_id=user_id, face_model=True)

    @blp.arguments(MultipartFileSchema, location="files")
    @blp.response(201, PhotoSchema)
    def post(self, files, user_id):
        user = UserModel.query.get_or_404(user_id)
        file_1 = files["file_1"]
        file_1.save(os.path.join(
            os.path.dirname(__file__),
            "..",
            "persons",
            user.company.id,
            user.username,
            secure_filename(file_1.filename)
        ))

        embedding = registration.get_embedding(
            user.company.id,
            user.username,
            secure_filename(file_1.filename)
        )

        if embedding is None:
            abort(500, message="Unable to find face in the photo")

        photo = PhotoModel(
            user_id=user.id,
            filename=secure_filename(file_1.filename),
            dir_path=os.path.join("/persons", user.company.id, user.username),
            url_path=os.path.join(
                "/static/person/",
                user.company.id,
                user.username,
                secure_filename(file_1.filename)),
            face_model=True
        )

        try:
            db.session.add(photo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting photo.")

        # make default avatar
        if user.avatar is None:
            user.avatar = photo.url_path
            try:
                db.session.add(user)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="An error occurred while inserting photo.")

        client.upsert(
            collection_name="Persons",
            points=[
                models.PointStruct(
                    id=f"{photo.id}",
                    vector=embedding.tolist(),
                    payload={
                        "username": user.username,
                        "company": user.company.id,
                    }
                )
            ]
        )



        return photo
