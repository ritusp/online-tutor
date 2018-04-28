from app import db
import datetime


class question_bank(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    grade = db.Column(db.String(20))
    subject = db.Column(db.String(20))
    question = db.Column(db.String(1000))
    detailed_answer = db.Column(db.String(5000))
    choice_1 = db.Column(db.String(200))
    choice_2 = db.Column(db.String(200))
    choice_3 = db.Column(db.String(200))
    choice_4 = db.Column(db.String(200))
    correct_answer = db.Column(db.String(200))

    def __init__(self, grade, subject, question, detailed_answer, choice_1, choice_2, choice_3, choice_4, correct_answer):
        self.grade = grade
        self.subject = subject
        self.question = question
        self.detailed_answer = detailed_answer
        self.choice_1 = choice_1     
        self.choice_2 = choice_2
        self.choice_3 = choice_3
        self.choice_4 = choice_4
        self.correct_answer = correct_answer

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(20))
    test = db.relationship('test_result', backref = 'user')

    def __init__(self, username, password):
        self.username = username
        self.password = password

class test_result(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    grade = db.Column(db.String(20))
    subject = db.Column(db.String(20))
    score = db.Column(db.Integer)
    total_questions = db.Column(db.Integer)
    test_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    question_id_list = db.Column(db.String(300))

    def __init__(self, grade, subject, score, total_questions, question_id_list):
        self.grade = grade
        self.subject = subject
        self.score = score
        self.total_questions = total_questions
        self.question_id_list = question_id_list
       