from app import db
from datetime import datetime, timezone
from .usermodel import User

# Is the title redundant?
class InfoModel(db.Model):
    __tablename__ = 'topicinfo'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, default=1)
    title = db.Column(db.String(255))
    seq = db.Column(db.Integer)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    # ToDo on initialisation make seq = 10*id
    
    def author_fullname(self):
        return User.get_fullname(self.author_id) 
    
    def dump(self):
        return { "id":self.id, "group":self.group, "title":self.title, "seq":self.seq, "content":self.content, 
          "author_id":self.author_id, "author_fullname":User.get_fullname(self.author_id) }
    

