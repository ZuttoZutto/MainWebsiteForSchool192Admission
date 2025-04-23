from cProfile import Profile

from flask_login import current_user
from flask_restful import abort

import flask
from flask import render_template
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams, UserClasses, Classes, Profiles, ExamsList
from forms.editexamform import EditExamForm
from tools.checks import check_user_role, current_user_role_name

blueprint = flask.Blueprint(
    'exams_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/timetable")
def timetable():
    if check_user_role() == 3:
        return render_template("timetable.html",
                               role_name=current_user_role_name())
    if check_user_role() == 1:
        class_message_list = []
        session = db_session.create_session()
        classes_ids = [row[0] for row in (session.query(UserClasses.ClassId)
                                          .filter(UserClasses.UserId == current_user.id)).all()]
        for class_id in classes_ids:
            class_ = session.query(Classes).get(class_id)
            class_profile_if = class_.ProfileId
            profile = (session.query(Profiles).get(class_profile_if)).Name
            text = (f"Вы указали, что хотите поступить в {class_.Number}{class_.Letter} класс с"
                    f" профилем {profile}, для этого вам нужно сдать"
                    f" эти вступительные экзамены:\n\n")
            exams_ids = [row[0] for row in (session.query(ExamsList.ExamId)
                                            .filter(ExamsList.ClassId == class_id)).all()]
            for exam_id in exams_ids:
                exam = session.query(Exams).get(exam_id)
                text += f"● {exam.Name}, проводится {exam.Date}\n"
            class_message_list.append(text)

        if not classes_ids:
            text = "Вы не выбрали ни одного класса, в который хотите поступить при регистрации."
            class_message_list.append(text)
        return render_template("directed_timetable.html",
                               role_name=current_user_role_name(),
                               class_list=class_message_list)
    else:
        return render_template("view_timetable.html",
                               role_name=current_user_role_name())

@blueprint.route('/exams/<int:exam_id>', methods=['GET', 'POST'])
def edit_exam(exam_id):
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            return redirect("/admission192/timetable")
        else:
            return render_template('edit_exam.html',
                                   title='Изменение данных экзамена',
                                   form=form, exam_id=exam_id,
                                   role_name=current_user_role_name())
    return abort(403, message="Forbidden")

@blueprint.route('/addexam', methods=['GET', 'POST'])
def add_exam():
    if check_user_role() == 3:
        form = EditExamForm()
        if form.validate_on_submit():
            return redirect("/admission192/timetable")
        return render_template('add_exam.html',
                               title='Добавление нового экзамена',
                               form=form, role_name=current_user_role_name())
    return abort(403, message="Forbidden")