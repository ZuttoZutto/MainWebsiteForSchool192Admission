from datetime import datetime

from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse
from werkzeug.http import http_date

from data import db_session
from data.database import DemoExams, Comments, Classes, ExamsList, Profiles

from tools.checks import check_user_role

parser = reqparse.RequestParser()
parser.add_argument("id", required=True)
parser.add_argument("Comment", required=True)
parser.add_argument("ExamId", required=True)
parser.add_argument("UserId", required=True)

class ProfileListResource(Resource):
    def get(self):
        session = db_session.create_session()
        profiles = session.query(Profiles).all()
        return jsonify([item.to_dict(
            only=("id", "Name")) for item in profiles])