from app import db
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from app import bcrypt, db, login_manager
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timezone
from .groupmodel import Group

class Permission:
    READ = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Guest': [Permission.READ],
            'Member': [Permission.READ, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.READ, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.READ, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    name = db.Column(db.String(32),nullable=False)
    current_group = db.Column(db.Integer, default=1)
    groups = db.relationship('Group', backref='founder', lazy='dynamic')
    topics = db.relationship('Topic', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    infos = db.relationship('Info', backref='owner', lazy='dynamic')


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['LP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    # Next pair of functions generate confirmation tokens with timestamp
    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return serializer.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    
    def confirm(self, token, expiration=3600): # 3 hours before expiry
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
            )
        except:
            return False
        #print("confirming email: ", email, "against ", self.email )
        if email != self.email:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    # Is there a better way of preventing data loss than increasing the expiry time? Concerned about conflict.
    def generate_reset_token(self, expiration=36000): # 10 hours to prevent loss of data while having lunch etc. ? possible data conflict?
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'id': self.id},salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def reset_password(token, new_password, expiration=3600):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            id = serializer.loads(
                token,
                salt=current_app.config['SECURITY_PASSWORD_SALT'],
                max_age=expiration
                )
        except:
            return False
        
        user = User.query.get(id)
        if user.id is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def fullname(self):
        return self.name.replace('_', ' ').strip()
    
    def firstname(self):
        n = self.name.split('_')
        return n[0]
    
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_guest(self):
        return self.can(Permission.READ)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    def is_member(self):
        return self.can(Permission.WRITE)
    
    def is_moderator(self):
        return self.can(Permission.MODERATE)
    
    # Groups the user is a member of as list of integers
    def mygrouplist(self):
        if self.groups is None:
            return []
        try:
            g = str(self.groups).split(',')
        except:     # single item
            return list( int(g) )
        return [ int(x) for x in g ] 
    
    def mygroupchoices(self):
        choices = []
        print( self.mygrouplist() )
        for i in self.mygrouplist():
            g = Group.query.filter_by(id=i).first()
            choices.append((g.id, g.groupname))
        print('choices: ',choices)
        return choices
        
    def addgroup(self, gp ):
        if not self.groups:
            self.groups='1'  # Mandatory Group
        #print('user: {},  groups: {}'.format(self.name, self.groups))
        if not gp in self.mygrouplist():
            g = str( self.groups )
            self.groups = g + ',' + str(gp)
        return 

    def removegroup(self, gp):
        mygrouplist = self.mygrouplist()
        if gp in mygrouplist:
            mygrouplist.remove(gp)
            mygroupliststr = [str(x) for x in mygrouplist ]
            self.groups = ','.join(mygroupliststr)
        return

    def current_groupname(self):
        gr = Group.query.get(self.current_group)
        return gr.groupname   

    def ping(self):
        self.last_seen = datetime.now(tz=timezone.utc)
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_fullname(user_id):
        return User.query.get(user_id).fullname()

    def __repr__(self):
        return f"<email {self.email}>"
    
    
class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_member(self):
        return False
    
    def is_moderator(self):
        return False

    def is_administrator(self):
        return False
    
    def current_groupname(self):
        return LP_GROUP_NAME

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
 
