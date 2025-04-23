from flask_login import current_user, AnonymousUserMixin
from flask import current_app
from data import db_session
from data.database import Users, Roles


def check_user_role():
    with current_app.app_context():
        if current_user.is_anonymous:
            return 0
        return current_user.RoleId

def current_user_role_name():
    with current_app.app_context():
        if current_user.is_anonymous:
            return 0
        session = db_session.create_session()
        user = session.query(Users).get(current_user.id)
        role_name = session.query(Roles).filter(Roles.id == user.RoleId).first().Role
        session.close()
        return role_name