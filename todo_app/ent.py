from datetime import datetime
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	name = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	task = db.relationship('Task', backref='author', lazy=True)


class Task(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(30), unique=True, nullable=False)
	content = db.Column(db.String(500), nullable=False)
	created_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	upd_dt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)