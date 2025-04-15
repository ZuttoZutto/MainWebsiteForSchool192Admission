from flask_restful import abort

import flask
from flask import render_template
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams
from forms.editexamform import EditExamForm
from tools.checks import check_user_role

blueprint = flask.Blueprint(
    'exams_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/timetable")
def timetable():
    if check_user_role() == 3:
        return render_template("timetable.html")
    return abort(403, message="Forbidden")

@blueprint.route('/exams/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            return redirect("/timetable")
        else:
            return render_template('edit_exam.html', title='Изменение данных экзамена', form=form, exam_id=exam_id)
    return abort(403, message="Forbidden")

@blueprint.route('/addexam', methods=['GET', 'POST'])
def add_exam():
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            return redirect("/timetable")
        return render_template('add_exam.html', title='Добавление нового экзамена', form=form)
    return abort(403, message="Forbidden")