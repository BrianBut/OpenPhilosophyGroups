import unittest
from datetime import datetime, timezone
from app import create_app, db
from app.models import TodoModel, User


class TodoModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_todo_default(self):
        t = TodoModel(content='test1', group=1)
        db.session.flush()
        self.assertTrue( t.content == 'test1')
        print(t.creation_datetime)
        self.assertTrue(t.group == 1)

    def test_todo_notdone_group(self):
        t = TodoModel( group=7, content="rhubarb")
        db.session.add( t )
        t = TodoModel( group=1, content="custard")
        db.session.add( t )
        t = TodoModel( group=1, content="horse manure")
        db.session.add( t )
        t = TodoModel( group=7, content="ice cream")
        db.session.add( t )
        t = TodoModel( group=7, content="rhubarb")
        db.session.add( t )
        db.session.commit()
        nd7 = TodoModel.notdone(7)
        #print("notdone: ", nd7)
        self.assertTrue( len(nd7) == 3)
        nd1 = TodoModel.notdone(1)
        self.assertTrue( len(nd1) == 2)
        nd2 = TodoModel.notdone(2)
        self.assertTrue( len(nd2) == 0)

    def test_todo_done_group(self):
        t = TodoModel( group=7, content="rhubarb", completion_datetime=datetime.now(tz=timezone.utc))
        db.session.add( t )
        t = TodoModel( group=1, content="custard")
        db.session.add( t )
        t = TodoModel( group=1, content="horse manure")
        db.session.add( t )
        t = TodoModel( group=7, content="ice cream")
        db.session.add( t )
        t = TodoModel( group=7, content="rhubarb")
        db.session.add( t )
        db.session.commit()
        d7 =  TodoModel.done(7)
        self.assertTrue( len(d7) == 1)

    def test_todo_easydate(self):
        t = TodoModel( group=7, content="rhubarb")
        db.session.add( t )
        db.session.commit()
        print('easydate: ',t.easydate())
        assert( t.easydate() is not None )
