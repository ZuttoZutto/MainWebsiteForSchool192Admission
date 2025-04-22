#from crypt import methods

from flask import g

from flask import Flask, render_template, jsonify, send_file, redirect, send_from_directory, request, url_for, \
    current_app, session
from werkzeug.test import Client
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from flask_restful import Api, abort

from tools.checks import check_user_role, current_user_role_name

from data import db_session
from data.database import Users, Exams, Parents, UserClasses, Classes, Profiles
from forms.editexamform import EditExamForm
from datetime import date

from forms.loginform import LoginForm
from forms.registerform import RegisterForm

from resources import (exam_resources, demo_resources, users_resources, subexam_resources,
                       usersmarks_resources, comment_resources, class_resources,
                       profile_resources, examslist_resources, parents_resources,
                       usersclasses_resources)

import requests

from blueprints import (exams_api, marks_api, messages_api, classes_api,
                        aboutschool_api, users_api)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

app.register_blueprint(exams_api.blueprint)
app.register_blueprint(marks_api.blueprint)
app.register_blueprint(messages_api.blueprint)
app.register_blueprint(classes_api.blueprint)
app.register_blueprint(aboutschool_api.blueprint)
app.register_blueprint(users_api.blueprint)

api.add_resource(demo_resources.DemoListResource, "/api/demo/")
api.add_resource(users_resources.UserResource, "/api/users/<int:user_id>/")
api.add_resource(users_resources.UsersListResource, "/api/users/")
api.add_resource(exam_resources.ExamsListResource, "/api/exams/")
api.add_resource(exam_resources.ExamResource, "/api/exams/<int:exam_id>/")
api.add_resource(subexam_resources.SubexamsListResource, "/api/subexams/")
api.add_resource(subexam_resources.SubexamResource, "/api/subexams/<int:subexam_id>/")
api.add_resource(usersmarks_resources.UsersMarksListResource, "/api/usersmarks/")
api.add_resource(usersmarks_resources.UsersMarksResource, "/api/usersmarks/<int:exam_id>/")
api.add_resource(comment_resources.CommentListResource, "/api/comments/")
api.add_resource(class_resources.ClassListResource, "/api/classes/")
api.add_resource(class_resources.ClassResource, "/api/classes/<int:class_id>/")
api.add_resource(profile_resources.ProfileListResource, "/api/profiles/")
api.add_resource(examslist_resources.ExamsListListResource, "/api/examslist/")
api.add_resource(examslist_resources.SingleEXAMSLISTResource, "/api/examslist/<int:class_id>/")
api.add_resource(parents_resources.ParentsListResource, "/api/parents/")
api.add_resource(usersclasses_resources.UserClassesListResource, "/api/userclasses/")
api.add_resource(usersclasses_resources.UserClassesResource, "/api/userclasses/<int:user_id>/")


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(Users, user_id)

@app.route("/")
def index():
    return render_template("index.html",
                           title="Главная страница-Сайт для поступления в школу №192",
                           check_user_function=check_user_role, role_name=current_user_role_name())

@app.route("/demoexams")
def demoexams():
    return render_template("demoexams.html", role_name=current_user_role_name())

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(Users).filter(Users.Email == form.email.data).first()
        if user:
            password = user.Password
            if user and form.password.data == password:
                login_user(user, remember=form.remember_me.data)
                return redirect("/admission192")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, role_name=current_user_role_name())
    return render_template('login.html', title='Авторизация', form=form, role_name=current_user_role_name())

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    return render_template('register.html', title='Регистрация', form=form,
                           role_name=current_user_role_name())

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/admission192")

@app.route('/g.png')
def download_g_png():
    return send_from_directory('static', 'g.png', as_attachment=True)

db_session.global_init("/var/www/Admission192/website/db/db.db")
if __name__ == "__main__":
    app.run()