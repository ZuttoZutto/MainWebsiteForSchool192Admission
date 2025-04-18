from datetime import datetime
from typing import List

from flask import session, jsonify, render_template, request
from flask_restful import Resource, abort, reqparse
from werkzeug.http import http_date

from data import db_session
from data.database import DemoExams, Comments, Classes, ExamsList

from tools.checks import check_user_role


class ClassListResource(Resource):
    def get(self):
        if check_user_role() == 3:
            session = db_session.create_session()
            classes = session.query(Classes).all()
            return jsonify([
                dict(
                    item.to_dict(only=("id", "Number", "Letter", "ProfileId")),
                    **{"ProfileName": item.profile.Name},
                ) for item in classes
            ])
        return abort(403, message="Forbidden")

    def post(self):
        if check_user_role() != 3:
            return abort(403, message="Forbidden")

        data = request.json

        # Работа с базой данных
        session = db_session.create_session()
        class_id = data["Class"]["id"]
        Class = session.query(Classes).filter(Classes.id == class_id).first()

        if not Class:
            return jsonify({"message": f"Класс с id={class_id} не найден"})

        # Обновляем данные класса
        Class.Letter = data["Class"]["letter"]
        Class.Number = data["Class"]["number"]
        Class.ProfileId = data["Class"]["profile_id"]

        # Работаем с существующими экзаменами
        existing_exams = [exam.id for exam in session.query(ExamsList.id).
        filter(ExamsList.ClassId == class_id).all()]

        for item in set(existing_exams) - set(data["Exams"]):
            exam_in_list = session.query(ExamsList).filter(ExamsList.id == item).first()
            session.delete(exam_in_list)

        for item in set(data["Exams"]) - set(existing_exams):
            exam_not_in_list = ExamsList(ClassId=class_id, ExamId=item)
            session.add(exam_not_in_list)

        session.commit()

        return jsonify({"message": "success"})

class ClassResource(Resource):
    def get(self, class_id):
        session = db_session.create_session()

        # Получаем класс по class_id
        cls = session.query(Classes).filter(Classes.id == class_id).first()

        if not cls:
            return jsonify({"error": "Класс не найден"})

        # Получаем список экзаменов, связанных с этим классом
        exams_list = session.query(ExamsList).filter(ExamsList.ClassId == class_id).all()

        # Строим словарь с экзаменами
        exams = {}
        for exam_item in exams_list:
            date = exam_item.exam.Date
            date = date.strftime("%Y-%m-%d")
            exams[exam_item.ExamId] = {
                "name": exam_item.exam.Name,
                "date": date
            }

        # Формируем финальную структуру JSON
        result = {
            "Class": {
                "id": cls.id,
                "number": cls.Number,
                "letter": cls.Letter,
                "profile_name": cls.profile.Name,
                "profile_id": cls.profile.id
            },
            "Exams": exams
        }
        print(result)

        return jsonify(result)