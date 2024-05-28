import os.path
from werkzeug.utils import secure_filename
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from qdrant_client.http import models

import face_recognition
from qdrant import client
from db import db
from models import PhotoModel, UserModel, RecognitionModel
from schemas import MultipartFileSchema, FormSchema, RecognitionSchema, RecognitionResultSchema

blp = Blueprint("Persons", __name__, description="Operations on persons")

registration = face_recognition.PersonRegistration()


@blp.route("/recognition/<string:username>")
class Recognition(MethodView):
    @blp.arguments(MultipartFileSchema, location="files")
    @blp.response(200, RecognitionSchema)
    def post(self, files, username):
        user = UserModel.query.filter_by(username=username).first_or_404()
        file_1 = files["file_1"]
        file_1.save(os.path.join(
            os.path.dirname(__file__),
            "..",
            "persons",
            user.company.id,
            user.username,
            secure_filename(file_1.filename)
        ))

        photo = PhotoModel(
            user_id=user.id,
            filename=secure_filename(file_1.filename),
            dir_path=os.path.join("/persons", user.company.id, user.username),
            url_path=os.path.join(
                "/static/person/",
                user.company.id,
                user.username,
                secure_filename(file_1.filename)),
            face_recognition=True
        )

        try:
            db.session.add(photo)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting photo.")

        embedding = registration.get_embedding(
            user.company.id,
            user.username,
            secure_filename(file_1.filename)
        )

        if embedding is None:
            abort(500, message="Unable to find face in the photo")

        results = client.search(
            collection_name="Persons",
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="username",
                        match=models.MatchValue(
                            value=user.username
                        )
                    ),
                    models.FieldCondition(
                        key="company",
                        match=models.MatchValue(
                            value=user.company.id
                        )
                    )
                ]
            ),
            search_params=models.SearchParams(hnsw_ef=128, exact=False),
            query_vector=embedding,
            limit=3
        )

        response = RecognitionSchema()
        response.username = user.username
        response.fullname = user.fullname
        response.company_id = user.company.id
        response.url_path = photo.url_path
        response.results = []

        matched_photo = None
        matched_score = None
        for res in results:
            if res.score > 0.6:
                matched = PhotoModel.query.get(res.id)
                if matched_photo is None:
                    matched_photo = matched.id
                if matched_score is None:
                    matched_score = res.score
                recognition_result = RecognitionResultSchema()
                recognition_result.score = res.score
                recognition_result.url_path = matched.url_path
                response.results.append(recognition_result)

        recognition = RecognitionModel(
            user_id=user.id,
            photo_id=photo.id,
            matched_photo_id=matched_photo,
            matched_score=matched_score
        )

        try:
            db.session.add(recognition)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting photo.")

        response.logged_at = recognition.logged_at

        return response

