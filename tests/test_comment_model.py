import unittest
from datetime import datetime, time
from app import create_app, db
from app.models import User, AnonymousUser, Role, Comment, User, Topic


class CommentModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_title(self):
        t = Comment(content="Test content")
        self.assertTrue(t.content == "Test content" )

    def test_creation_datetime(self):
        t = Comment(content="Test Topic")
        db.session.add(t)
        db.session.commit()
        t2 = Comment.query.first()
        #print("t.creation_datetime: {}".format(t2.creation_datetime))
        self.assertTrue(t2.creation_datetime is not None)

    def test_comment_author(self):
        u = User(email='me@my.home', password='cheese', name='Brian')
        db.session.add( u )
        db.session.commit()
        c = Comment(content='Still Testing', author_id=u.id)
        db.session.add(c)
        db.session.commit()
        print( c.author_name() )
        self.assertTrue( c.author_name() == 'Brian')
    '''
    
    #def test_markdown(self):
    '''
    