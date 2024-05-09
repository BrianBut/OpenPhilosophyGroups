from app import db

class GroupDoes:
    INFO = 1
    TODO = 2
    ONLINE = 4
    MEETING = 8
    REGISTRATION = 16 # Only member who are on the register can see these groups
    NECESSARY = 32

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    activities = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        if self.activities is None:
            self.activities = GroupDoes.ONLINE

    def add_activity( self, av ):
        self.activities = self.activities | av

    def remove_activity( self, av):
        self.activities = ( not av ) & self.activities 


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(128), unique=True, nullable=False, default='Phil')
    category = db.Column(db.Integer, default=8) 

    @staticmethod
    def insert_default_group():
        group = Group(groupname='Philosphy Groups')
        db.session.add( group )
        db.session.commit()
