from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse

from data import db_session
from data.database import Exams, Messages
from datetime import date
from tools.checks import check_user_role


class MessageListResource(Resource):
    def get(self):
        if check_user_role() >= 1:
            session = db_session.create_session()
            exams = session.query(Messages).all()
            return jsonify([item.to_dict(
                only=("id", "Name", "Date")) for item in exams])
        return abort(403, message="Forbidden")