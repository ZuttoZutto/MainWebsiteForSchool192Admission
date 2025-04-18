from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.database import DemoExams, Comments

parser = reqparse.RequestParser()
parser.add_argument("id", required=True)
parser.add_argument("Comment", required=True)
parser.add_argument("ExamId", required=True)
parser.add_argument("UserId", required=True)

class CommentListResource(Resource):
    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        existing_comment = session.query(Comments).filter(Comments.id == args["id"]).first()
        comment = args["Comment"].rstrip().lstrip()
        if existing_comment:
            if comment:
                existing_comment.Comment = comment
            else:
                session.delete(existing_comment)
            session.commit()
            return jsonify({"id": existing_comment.id})
        else:
            if comment:
                new_comment = Comments(
                    UserId=args["UserId"],
                    ExamId=args["ExamId"],
                    Comment=comment
                )
                session.add(new_comment)
                session.commit()
                return jsonify({"id": new_comment.id})