from app import db
from datetime import datetime, timezone

def easydate( dt ):
        date = datetime.date( dt )
        return date.strftime("%a %d %b %Y")

from .usermodel import User

class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, default=1)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    completion_datetime = db.Column(db.DateTime, default=datetime.max)
    
    def author_fullname(self):
        return User.get_fullname(self.author_id) 
    
    
    
    def dump(self):
        return { "id":self.id, "group":self.group, "content":self.content, 
          "author_id":self.author_id, 
          "creation_datetime":easydate(self.creation_datetime), 
          "completion_datetime":easydate(self.completion_datetime )}
          #"author_fullname":User.get_fullname(self.author_id) }
    
    @staticmethod
    def notdone(group_id):
        rv = []
        for todo in TodoModel.query.filter_by( group = group_id, completion_datetime = datetime.max).order_by('creation_datetime').all():
            rv.append( todo.dump() )
        return rv

    @staticmethod
    def done(group_id):
        rv = []
        for todo in TodoModel.query.filter_by( group = group_id).filter( TodoModel.completion_datetime !=  datetime.max).order_by('creation_datetime').limit(100).all():
            rv.append( todo.dump() )
        return rv