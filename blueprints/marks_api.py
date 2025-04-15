from flask_restful import abort

import flask
from flask import render_template
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams
from forms.editexamform import EditExamForm
from tools.checks import check_user_role

blueprint = flask.Blueprint(
    'marks_api',
    __name__,
    template_folder='templates'
)

@blueprint.route("/choose_exam_for_mark")
def chose_exam_for_mark():
    if check_user_role() >= 2:
        return render_template("choose_exam_for_mark.html")
    return abort(403, message="Forbidden")

@blueprint.route("/put_marks_for/<int:exam_id>")
def put_mark_for_exam(exam_id):
    if check_user_role() >= 2:
        return render_template("put_marks.html", exam_id=exam_id)
    return abort(403, message="Forbidden")