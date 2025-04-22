from flask import session, jsonify, render_template, request
from flask_restful import Resource, abort, reqparse
from sqlalchemy.testing.suite.test_reflection import users

from data import db_session
from data.database import Exams, Users, Parents


class ParentsListResource(Resource):
    def post(self):
        session = db_session.create_session()
        data = request.json
        existing_parent = (session.query(Parents)
                         .filter((Parents.Name == data["Name"]) &
                                 (Parents.Surname == data["Surname"]) &
                                 (Parents.Phone == data["Phone"]) &
                                 (Parents.Email == data["Email"])).first())
        if existing_parent:
            return jsonify({"id": existing_parent.id})
        parent = Parents(
            Name=data["Name"],
            Surname=data["Surname"],
            Phone=data["Phone"],
            Email=data["Email"],
        )
        session.add(parent)
        session.commit()
        return jsonify({"id": parent.id})