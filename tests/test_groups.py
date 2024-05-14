import sys
import unittest
import time
from datetime import datetime, timezone
from app import create_app, db
from app.models import Group, GroupDoes


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_default_group(self):
        group = Group(groupname = 'Phil')
        #print('groupname, ',group.groupname)
        self.assertTrue(group.groupname == 'Phil', group.category == GroupDoes.INFO) 

    def test_info_group(self):
        group = Group(groupname = 'Phil', category = GroupDoes.INFO)
        self.assertTrue( group.is_info() )
        self.assertFalse( group.is_online_only())

    def test_todo_group(self):
        group = Group(groupname = 'Phil', category = GroupDoes.TODO)
        self.assertTrue( group.is_todo())
        self.assertFalse( group.is_info() )
        self.assertFalse( group.is_online_only())