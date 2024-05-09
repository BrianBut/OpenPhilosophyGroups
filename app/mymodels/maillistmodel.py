from app import db
from datetime import datetime, timezone

class MailList(db.Model):
    __tablename__ = 'maillist'
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.Integer)
    email = db.Column(db.String(64), unique=True, index=True)
    datetime = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))

    @staticmethod
    def is_member(email):
        approved = MailList.query.filter_by(email=email).first()
        return approved