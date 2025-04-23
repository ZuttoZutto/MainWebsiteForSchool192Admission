from flask import session, jsonify, render_template, request
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.database import DemoExams, Comments, ExamsList
from tools.checks import check_user_role


class SingleEXAMSLISTResource(Resource):
    def delete(self, class_id):
        if check_user_role() != 3:
            return abort(403, message="Forbidden")
        data = request.json
        exam_id = data["ExamId"]
        session = db_session.create_session()
        examslist = session.query(ExamsList).filter((ExamsList.ClassId == class_id) &
                                        (ExamsList.ClassId == class_id)).first()
        session.delete(examslist)
        session.commit()


class ExamsListListResource(Resource):
    def post(self):
        if check_user_role() != 3:
            return abort(403, message="Forbidden")
        data = request.json
        session = db_session.create_session()
        existing_examslist = session.query(ExamsList).filter((ExamsList.ClassId == data["ClassId"])
                                                             & (ExamsList.ExamId == data["ExamId"])).first()
        if not existing_examslist:
            examslist = ExamsList(
                ClassId=data["ClassId"],
                ExamId=data["ExamId"]
            )
            session.add(examslist)
            session.commit()
            return jsonify({"message": "success"})
        return jsonify({"message": "this examslist already exists"})
