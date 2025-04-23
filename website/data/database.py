from flask_login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase as Base

class Users(Base, UserMixin, SerializerMixin):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Phone = Column(String, unique=True, nullable=False)
    LastSchool = Column(String, nullable=False)
    Name = Column(String, nullable=False)
    Surname = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    ParentId = Column(Integer, ForeignKey('Parents.id'), nullable=False)
    Column(Date, nullable=False)
    RoleId = Column(Integer, ForeignKey('Roles.id'), nullable=False)
    Password = Column(String, nullable=False)

    parent = relationship('Parents')
    role = relationship('Roles')

    comments = relationship("Comments", back_populates='user')
    messages = relationship("Messages", back_populates='user')
    marks = relationship("MarksList", back_populates='user')
    complete_classes = relationship("StudentsList", back_populates='user')
    desired_classes = relationship("UserClasses", back_populates='user')
    additional_information = relationship("AdditionalInformation",
                                          back_populates='user')


class Classes(Base, SerializerMixin):
    __tablename__ = 'Classes'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ProfileId = Column(Integer, ForeignKey('Profiles.id'), nullable=False)
    Number = Column(Integer, nullable=False)
    Letter = Column(String)

    profile = relationship('Profiles')

    exams = relationship("ExamsList", back_populates='classs')
    completed_users = relationship("StudentsList", back_populates='classs')
    desired_users = relationship("UserClasses", back_populates='classs')


class Exams(Base, SerializerMixin):
    __tablename__ = 'Exams'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, unique=True, nullable=False)
    Date = Column(Date, nullable=False)

    class_exams = relationship("ExamsList", back_populates='exam')
    subexams = relationship("Subexams", back_populates='exam')
    comments = relationship("Comments", back_populates='exam')

class Profiles(Base, SerializerMixin):
    __tablename__ = 'Profiles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, unique=True, nullable=False)

    classes = relationship("Classes", back_populates='profile')

class Messages(Base, SerializerMixin):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    TitleId = Column(Integer, ForeignKey('MessageTitles.id'), nullable=False)
    TextId = Column(Integer, ForeignKey('MessageTexts.id'), nullable=False)
    Date = Column(Date, nullable=False)

    user = relationship('Users')
    title = relationship('MessageTitles')
    text = relationship('MessageTexts')

class Parents(Base):
    __tablename__ = 'Parents'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, nullable=False)
    Surname = Column(String, nullable=False)
    Phone = Column(String, nullable=False)
    Email = Column(String, nullable=False)

    users = relationship("Users", back_populates='parent')

class Roles(Base):
    __tablename__ = 'Roles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Role = Column(String, unique=True, nullable=False)

    users = relationship("Users", back_populates='role')

class MarksList(Base):
    __tablename__ = 'MarksList'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    SubexamId = Column(Integer, ForeignKey('Subexams.id'), nullable=False)
    Date = Column(Date, nullable=False)
    Mark = Column(Numeric, nullable=False)

    user = relationship('Users')
    subexam = relationship('Subexams')


class ExamsList(Base, SerializerMixin):
    __tablename__ = 'ExamsList'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ClassId = Column(Integer, ForeignKey('Classes.id'), nullable=False)
    ExamId = Column(Integer, ForeignKey('Exams.id'), nullable=False)

    classs = relationship('Classes')
    exam = relationship('Exams')


class DemoExams(Base, SerializerMixin):
    __tablename__ = 'DemoExams'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, unique=True, nullable=False)
    FilePath = Column(String, nullable=False)


class StudentsList(Base):
    __tablename__ = 'StudentsList'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    ClassId = Column(Integer, ForeignKey('Classes.id'), nullable=False)

    user = relationship('Users')
    classs = relationship('Classes')


class MessageTitles(Base):
    __tablename__ = 'MessageTitles'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Title = Column(String)

    messages = relationship("Messages", back_populates='title')


class MessageTexts(Base):
    __tablename__ = 'MessageTexts'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Text = Column(String)

    messages = relationship("Messages", back_populates='text')


class Comments(Base):
    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ExamId = Column(Integer, ForeignKey('Exams.id'), nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    Comment = Column(String, nullable=False)

    exam = relationship('Exams')
    user = relationship('Users')


class UserClasses(Base):
    __tablename__ = 'UserClasses'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    ClassId = Column(Integer, ForeignKey('Classes.id'), nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)

    classs = relationship('Classes')
    user = relationship('Users')


class AdditionalInformation(Base):
    __tablename__ = 'AdditionalInformation'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    UserId = Column(Integer, ForeignKey('Users.id'), nullable=False)
    Information = Column(Integer, nullable=False)

    user = relationship('Users')


class Subexams(Base, SerializerMixin):
    __tablename__ = 'Subexams'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    Name = Column(String, nullable=False)
    ExamId = Column(Integer, ForeignKey('Exams.id'), nullable=False)
    NumberOfSubexam = Column(Integer, nullable=False)

    exam = relationship('Exams')

    marks = relationship("MarksList", back_populates='subexam')