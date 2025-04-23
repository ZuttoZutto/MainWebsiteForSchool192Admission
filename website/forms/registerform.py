from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.fields.simple import TelField
from wtforms.validators import DataRequired, ValidationError, Length

import re


class RegisterForm(FlaskForm):
    name = StringField('Имя абитуриента', validators=[DataRequired()])
    surname = StringField('Фамилия абитуриента', validators=[DataRequired()])
    phone = TelField('Номер телефона абитуриента', validators=[
        DataRequired(),
        lambda form, field: validate_phone(field.data)
    ])
    email = EmailField('Адрес электронной почты абитуриента', validators=[DataRequired()])
    last_school = StringField('Название или номер школы, в которой вы учитесь', validators=[DataRequired()])
    # about = TextAreaField("Немного о себе")
    password = PasswordField(
        label="Придумайте пароль для входа в свою учетную запись",
        validators=[
            DataRequired(message="Пароль обязателен"),
            Length(min=8, message="Минимальная длина пароля — 8 символов")
        ]
    )
    parent_name = StringField('Имя родителя', validators=[DataRequired()])
    parent_surname = StringField('Фамилия родителя', validators=[DataRequired()])
    parent_phone = TelField('Номер телефона родителя', validators=[
        DataRequired(),
        lambda form, field: validate_phone(field.data)
    ])
    parent_email = EmailField('Адрес электронной почты родителя', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироватся')


def validate_phone(phone_number):
    """
    Валидатор номера телефона
    Формат: '+79XXXXXXXXX' или '89XXXXXXXXX'
    """
    pattern = r'^(\+7|8)?9\d{9}$'
    if not re.match(pattern, phone_number):
        raise ValidationError('Введён некорректный номер телефона. '
                              'Формат: "+79XXXXXXXXX" или "89XXXXXXXXX".')