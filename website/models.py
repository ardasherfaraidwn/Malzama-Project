from datetime import timezone
from enum import unique
from . import db
from sqlalchemy.sql import func



class Students(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    st_name = db.Column(db.String(255),unique=True)
    infos = db.relationship('info')

class Malzama_tp(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    typee = db.Column(db.String(200))

class Malzama(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mz_name = db.Column(db.String(300))
    mz_category = db.Column(db.Integer,db.ForeignKey('malzama_tp.id'))
    infos = db.relationship('info')
    malzama_typpes = db.relationship('Malzama_tp')


class info(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('students.id'))
    malzama_id = db.Column(db.Integer,db.ForeignKey('malzama.id'))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
