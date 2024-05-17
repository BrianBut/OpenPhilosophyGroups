import unittest
from datetime import datetime, timezone
from app import create_app, db
from app.models import Todos, User


class TodoTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_todo_easydate(self):
        t = Todos( content="rhubarb")
        db.session.add( t )
        db.session.commit()
        #print('easydate: ',easydate())
        self.assertTrue( t.creation_datetime is not None )
        self.assertTrue( t.completion_datetime is not None )
