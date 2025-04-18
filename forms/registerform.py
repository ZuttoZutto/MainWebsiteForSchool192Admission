from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    phone = TelField('Номер телефона', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    last_school = StringField('Название или номер школы, из которой уходите', validators=[DataRequired()])
    parent_name = StringField('Имя родителя', validators=[DataRequired()])
    parent_surname = StringField('Фамилия родителя', validators=[DataRequired()])
    parent_phone = TelField('Номер телефона родителя', validators=[DataRequired()])
    parent_email = EmailField('Почта родителя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')