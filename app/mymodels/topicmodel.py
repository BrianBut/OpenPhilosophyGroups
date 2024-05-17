from app import db
from .usermodel import User
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__= 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    edit_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    def topic_title(self):
        return Topic.query.get(self.topic_id).title
    
    def author_name(self):
        return User.get_fullname(self.author_id)

    def dump(self):
        return { "id":self.id, "content":self.content, "topic_id":self.topic_id, "topic_title":self.topic_title(), "author_name":self.author_name() }



class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, default=1)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    last_edited_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    discussion_datetime = db.Column(db.DateTime, default=datetime.min)
    published = db.Column(db.Boolean, default=False)

    def discussion_date(self):
        if self.discussion_datetime == datetime.min:
            return "undecided"
        if self.discussion_datetime == datetime.max:
            return "never"
        return self.discussion_datetime.strftime('%a %d %b %Y')

    def discussion_time(self):
        if self.discussion_datetime:
            return self.discussion_datetime.strftime('%I:%M%p')
        return ""
    
    def author_fullname(self):
        return User.get_fullname(self.author_id) 

    def discussion_venue(self):
        if int(self.published) == 1:
            return 'online'
        elif int(self.published) == 2:
            return 'private'
        elif int(self.published) == 3:
            return 'info'
        if self.discussion_datetime == datetime.min:
            return 'proposed'
        if self.discussion_datetime < datetime.now(tz=timezone.utc):
            return 'past'
        return 'planned'
    
    def dump(self):
        return { "id":self.id, "group":self.group, "title":self.title, "summary":self.summary, "content":self.content, "published":self.published, "venue":self.discussion_venue(),
            "discussion_date":self.discussion_date(), "discussion_time":self.discussion_time(),  "author_id":self.author_id, "author_fullname":User.get_fullname(self.author_id) }
    