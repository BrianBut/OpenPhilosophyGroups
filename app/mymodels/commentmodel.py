from app import db
from .usermodel import User
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__= 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    topic_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    creation_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    def author_fullname(self):
        return User.get_fullname(self.author_id) 
