from flask import session, jsonify, render_template, request
from flask_restful import Resource, abort, reqparse
from sqlalchemy.orm import aliased
from sqlalchemy_serializer.lib.serializable import Decimal

import logging

from data import db_session
from data.database import Exams, MarksList, Subexams, Users, Parents, Comments, UserClasses, Classes
from datetime import date, datetime
from tools.checks import check_user_role

class UserClassesListResource(Resource):
    def post(self):
        data = request.json
        session = db_session.create_session()
        session.query(UserClasses).filter(
            UserClasses.UserId == data['UserId']
        ).delete()

        # Добавляем новые записи
        for class_id in data['Classes']:
            user_class = UserClasses(
                UserId=data['UserId'],
                ClassId=class_id
            )
            session.add(user_class)

        session.commit()
        return jsonify({"message": "success"})

class UserClassesResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        class_ids = [row[0] for row in session.query(UserClasses.ClassId)
        .filter(UserClasses.UserId == user_id).all()]
        return jsonify({"Classes": class_ids})