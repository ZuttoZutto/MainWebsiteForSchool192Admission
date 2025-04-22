from flask_restful import abort

import flask
from flask import render_template
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams
from forms.editexamform import EditExamForm
from tools.checks import check_user_role, current_user_role_name

blueprint = flask.Blueprint(
    'aboutschool_api',
    __name__,
    template_folder='templates'
)

@blueprint.route("/about_school")
def chose_class():
    return render_template("about_school.html",
                           role_name=current_user_role_name())