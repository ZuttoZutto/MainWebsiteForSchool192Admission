from flask import session, jsonify, render_template
from flask_restful import Resource, abort, reqparse
from sqlalchemy.orm import aliased
from sqlalchemy_serializer.lib.serializable import Decimal

import logging

from data import db_session
from data.database import Exams, MarksList, Subexams, Users, Parents, Comments
from datetime import date, datetime
from tools.checks import check_user_role

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

parser = reqparse.RequestParser()
parser.add_argument("UserId", required=True)
parser.add_argument("SubexamId", required=True)
parser.add_argument("Mark", required=True)


class UsersMarksResource(Resource):
    def get(self, exam_id):
        if check_user_role() >= 2:
            session = db_session.create_session()

            # Получаем всех пользователей
            users_query = session.query(Users.id, Users.Name, Users.Surname, Users.Email, Parents.Phone). \
                outerjoin(Parents, Users.ParentId == Parents.id). \
                all()

            users = {
                user_id: {
                    'User': {
                        'id': user_id,
                        'Name': user_name,
                        'Surname': user_surname,
                        'Email': user_email,
                        'ParentPhone': parent_phone,
                        'comment': {  # Изначально создаем пустой объект для комментария
                            'text': '',
                            'comment_id': None
                        }
                    },
                    'Subexams': {}
                } for user_id, user_name, user_surname, user_email, parent_phone in users_query
            }

            # Формулируем SQL-запрос для получения оценок и комментариев
            query = (
                session.query(
                    Users.Name.label('Name'),
                    Users.id.label('UserId'),
                    Subexams.Name.label('SubexamName'),
                    Subexams.id.label('SubexamId'),
                    MarksList.Mark.label('Mark'),
                    MarksList.id.label('MarkId'),  # Добавляем поле MarkId
                    Comments.id.label('CommentId'),  # Добавляем поле CommentId
                    Comments.Comment.label('Comment'),  # Добавляем комментарии
                    Comments.ExamId.label('ExamId')  # Добавляем поле ExamId
                )
                .filter(Subexams.ExamId == exam_id)
                .outerjoin(MarksList, MarksList.SubexamId == Subexams.id)
                .outerjoin(Users, Users.id == MarksList.UserId)
                .outerjoin(Comments, Comments.UserId == Users.id)  # Присоединяем комментарии по UserId
            )

            # Выполняем запрос и группируем результаты
            for result in query.all():
                if result.UserId in users:
                    # Проверяем, что оценка не равна None
                    if result.Mark is not None:
                        users[result.UserId]['Subexams'][result.SubexamId] = {
                            'Name': result.SubexamName,
                            'Mark': float(result.Mark),
                            'MarkId': result.MarkId  # Добавляем MarkId
                        }
                    else:
                        # Если оценка равна None, устанавливаем значение по умолчанию (например, 0.0)
                        users[result.UserId]['Subexams'][result.SubexamId] = {
                            'Name': result.SubexamName,
                            'Mark': 0.0,
                            'MarkId': None  # MarkId также будет None, если оценки нет
                        }

                    # Добавляем комментарий в словарь пользователя, если он совпадает с условиями
                    if result.CommentId is not None and result.ExamId == exam_id:
                        users[result.UserId]['User']['comment'] = {
                            'text': result.Comment,
                            'comment_id': result.CommentId
                        }

            # Формируем итоговый список данных для рендеринга
            rows = list(users.values())

            # Формируем список уникальных субэкзаменов в виде словарей
            subexams = (
                session.query(Subexams)
                .filter(Subexams.ExamId == exam_id)
                .order_by(Subexams.id)
                .with_entities(Subexams.id, Subexams.Name)
                .all()
            )
            subexams = [{'id': subexam_id, 'Name': subexam_name} for subexam_id, subexam_name in subexams]

            print({
                'rows': rows,
                'subexams': subexams
            })

            return jsonify({
                'rows': rows,
                'subexams': subexams
            })
        return abort(403, message="Forbidden")


class UsersMarksListResource(Resource):
    def post(self):
        if check_user_role() >= 2:
            session = db_session.create_session()
            args = parser.parse_args()
            user_id = args['UserId']
            subexam_id = args['SubexamId']
            mark = args['Mark']

            # Логируем получение параметров
            logging.debug(f"Параметры запроса: UserId={user_id}, SubexamId={subexam_id}, Mark={mark}")

            # Проверяем, существует ли запись с такими UserId и SubexamId
            existing_record = session.query(MarksList).filter(
                MarksList.UserId == user_id,
                MarksList.SubexamId == subexam_id
            ).first()

            # Логируем результат поиска записи
            if existing_record:
                logging.info(f"Найдена существующая запись с UserId={user_id} и SubexamId={subexam_id}")
            else:
                logging.info(f"Запись с UserId={user_id} и SubexamId={subexam_id} не найдена")

            if existing_record:
                # Обновляем существующую запись
                if mark:
                    existing_record.Mark = mark
                    existing_record.Date = datetime.now()
                    logging.info(f"Запись с UserId={user_id} и SubexamId={subexam_id} успешно обновлена")
                else:
                    comment = session.query(Comments).filter(Comments.MarkId == existing_record.id).first()
                    if comment:
                        session.delete(comment)
                    session.delete(existing_record)
                session.commit()
                return jsonify({"id": existing_record.id})
            else:
                # Создаем новую запись
                new_record = MarksList(
                    UserId=user_id,
                    SubexamId=subexam_id,
                    Mark=mark,
                    Date=datetime.now()
                )
                session.add(new_record)
                session.commit()
                logging.info(f"Создана новая запись с UserId={user_id} и SubexamId={subexam_id}")
                return jsonify({"id": new_record.id})
        else:
            logging.warning("Роль пользователя не позволяет выполнить операцию")
        return abort(403, message="Forbidden")