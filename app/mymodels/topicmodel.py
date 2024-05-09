from app import db
from flask import url_for
from datetime import datetime, timezone
from .usermodel import User

class Topic(db.Model):
    __tablename__ = 'topics'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer, default=1)
    title = db.Column(db.String(255))
    summary = db.Column(db.Text)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creation_datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    discussion_datetime = db.Column(db.DateTime, default=datetime.min)
    published = db.Column(db.Integer, default=0)
    online_only = db.Column(db.Boolean, default=False)

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
    
    @staticmethod
    def get_topics( group ):
        tl = { 'proposed_topics':[], 'future_topics':[], 'past_topics':[], 'online_topics':[], 'private_topics':[], 'todo_topics':[], 'info_topics':[] }
        topics = Topic.query.filter_by(group=group).order_by(Topic.discussion_datetime).all()
        for topic in topics:
            tt = topic.dump()
            tt['url'] = url_for('main.topic', topic_id=topic.id )
            if tt['venue'] == 'private': 
                tl['private_topics'].append(tt)
            elif tt['venue'] == 'proposed':
                tl['proposed_topics'].append(tt)
            elif tt['venue'] == 'online':
                tl['online_topics'].append(tt)
            elif tt['venue'] == 'planned':
                tl['future_topics'].append(tt)
            elif tt['venue'] == 'past':
                tl['past_topics'].append(tt)
            elif tt['venue'] == 'todos':
                tl['todo_topics'].append(tt)
            elif tt['venue'] == 'info':
                tl['info_topics'].append(tt)    
            else: 
                raise Exception("get_topics() failed to find venue: {}".format(tt['venue']) ) 
        return tl
