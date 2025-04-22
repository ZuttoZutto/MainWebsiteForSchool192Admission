from contextlib import contextmanager

from flask_login import current_user
from flask_restful import abort

import flask
from flask import render_template, session
from sqlalchemy.orm import joinedload
from werkzeug.utils import redirect

from data import db_session
from data.database import Exams, Users, Parents, Roles
from forms.edit_account_form import EditAccountForm
from tools.checks import check_user_role, current_user_role_name

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)

@blueprint.route("/account", methods=['GET', 'POST'])
def edit_account():
    form = EditAccountForm()

    session = db_session.create_session()
    # Загружаем пользователя и его роль за один запрос
    user = session.query(Users).get(current_user.id)
    parent = user.parent

    # Обработчик отправки формы
    if form.validate_on_submit():
        if form.old_password.data == user.Password:
            if not (parent.Name == form.parent_name.data and
                    parent.Surname == form.parent_surname.data and
                    parent.Phone == form.parent_phone.data and
                    parent.Email == form.parent_email.data):
                # Создаем нового родителя, если данные отличаются
                new_parent = Parents(
                    Name=form.parent_name.data,
                    Phone=form.parent_phone.data,
                    Email=form.parent_email.data,
                    Surname=form.parent_surname.data,
                )
                session.add(new_parent)
                session.flush()  # flush для получения временного id
                parent_id = new_parent.id
            else:
                parent_id = parent.id

            # Обновляем данные пользователя
            user.Name = form.name.data
            user.Email = form.email.data
            user.Phone = form.phone.data
            user.LastSchool = form.last_school.data
            user.Surname = form.surname.data
            user.ParentId = parent_id
            user.Password = form.new_password.data

            session.commit()
            return render_template('edit_account.html', title='Профиль пользователя',
                                   form=form, role_name=current_user_role_name(),
                                   success_message="Изменения успешно внесены")
        else:
            return render_template('edit_account.html', title='Профиль пользователя',
                                   form=form, role_name=current_user_role_name(),
                                   message="Неверно введён старый пароль")
    else:
        # Загружаем данные в форму
        form.name.data = user.Name
        form.surname.data = user.Surname
        form.phone.data = user.Phone
        form.email.data = user.Email
        form.new_password.data = user.Password
        form.last_school.data = user.LastSchool
        form.parent_name.data = parent.Name
        form.parent_surname.data = parent.Surname
        form.parent_phone.data = parent.Phone
        form.parent_email.data = parent.Email
        return render_template('edit_account.html', title='Профиль пользователя',
                       form=form, role_name=current_user_role_name())