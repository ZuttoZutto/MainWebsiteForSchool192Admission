from flask import session, jsonify, render_template, request
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
    def post(self):
        session = db_session.create_session()
        data = request.json
        existing_user = session.query(Users).filter(Users.Email == data["Email"]).first()
        if existing_user:
            return abort(400, message="Пользователь с таким адресом"
                                       " электронной почты уже есть")
        user = Users(
            Name=data["Name"],
            Surname=data["Surname"],
            Phone=data["Phone"],
            Email=data["Email"],
            LastSchool=data["LastSchool"],
            Password=data["Password"],
            ParentId=data["ParentId"],
            RoleId=1
        )
        session.add(user)
        session.commit()
        return jsonify({"id": user.id})


class UserResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        return jsonify(user.to_dict(
            only=("Phone", "LastSchool", "Email", "Name", "Surname",
                  "Password", "ParentId", "RoleId")))
    def delete(self, user_id):
        from app import logout
        logout()
        session = db_session.create_session()
        user = session.query(Users).get(user_id)
        for comment in user.comments:
            session.delete(comment)
        for message in user.messages:
            session.delete(message)
        for mark in user.marks:
            session.delete(mark)
        for complete_class in user.complete_classes:
            session.delete(complete_class)
        for desired_class in user.desired_classes:
            session.delete(desired_class)
        for additional_information in user.additional_information:
            session.delete(additional_information)
        session.delete(user)
        session.commit()