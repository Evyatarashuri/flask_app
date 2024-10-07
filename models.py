from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)