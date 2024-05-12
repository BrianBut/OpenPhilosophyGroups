import sys
import unittest
import time
from datetime import datetime, timezone
from app import create_app, db
from app.models import Group, Category


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

    def test_default_groups(self):
        group = Group(groupname = 'Phil')
        #print('groupname, ',group.groupname)
        self.assertTrue(group.groupname == 'Phil') 
