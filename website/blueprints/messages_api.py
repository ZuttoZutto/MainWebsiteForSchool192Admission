from flask_restful import abort

import flask
from flask import render_template
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams
from forms.editexamform import EditExamForm
from tools.checks import check_user_role, current_user_role_name

blueprint = flask.Blueprint(
    'messages_api',
    __name__,
    template_folder='templates'
)

@blueprint.route("/send_message")
def choose_user_for_message():
    if check_user_role() >= 3:
        return render_template("choose_user_for_message.html",
                               role_name=current_user_role_name())
    return abort(403, message="Forbidden")

@blueprint.route("/messages")
def users_messages():
    return render_template("users_messages.html",
                           role_name=current_user_role_name())