from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse
from sqlalchemy.testing.suite.test_reflection import users

from data import db_session
from data.database import Exams, Users


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(Users).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")

parser = reqparse.RequestParser()
parser.add_argument("id", required=True)
parser.add_argument("Name", required=True)
parser.add_argument("Date", required=True)

class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(Users).all()
        return jsonify([item.to_dict(
            only=("Name", "Surname", "")) for item in users])

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        exam = Exams(
            id=args["id"],
            Name=args["Name"],
            Date=args["Date"]
        )
        session.add(exam)
        session.commit()
        return jsonify({"id": exam.id})


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        return jsonify(user.to_dict(
            only=("Phone", "LastSchool", "Email", "Name", "Surname", "ParentId", "RoleId")))