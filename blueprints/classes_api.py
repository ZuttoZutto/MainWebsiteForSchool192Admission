from flask_restful import abort

import flask
from flask import render_template
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams
from forms.editexamform import EditExamForm
from tools.checks import check_user_role

blueprint = flask.Blueprint(
    'classes_api',
    __name__,
    template_folder='templates'
)

@blueprint.route("/classes")
def chose_class():
    if check_user_role() >= 3:
        return render_template("classes_list.html")
    return abort(403, message="Forbidden")

@blueprint.route("/classes/<int:class_id>")
def edit_class(class_id):
    if check_user_role() >= 3:
        return render_template("edit_class.html")
    return abort(403, message="Forbidden")

@blueprint.route('/from_classes_exams/<int:class_id>/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(class_id, exam_id):
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            return redirect(f"/classes/{class_id}")
        else:
            return render_template('edit_exam.html', title='Изменение данных экзамена', form=form, exam_id=exam_id)
    return abort(403, message="Forbidden")

@blueprint.route("/choose_exam_for_class/<int:class_id>")
def choose_exam(class_id):
    if check_user_role() >= 3:
        return render_template("choose_exam_for_class.html", class_id=class_id)
    return abort(403, message="Forbidden")

@blueprint.route("/add_class")
def add_class(class_id):
    if check_user_role() >= 3:
        return render_template("add_class.html")
    return abort(403, message="Forbidden")