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

    def test_default_group(self):
        group = Group(groupname = 'Phil', founder = 1)
        #print('groupname, ',group.groupname)
        self.assertTrue(group.groupname == 'Phil', group.category == 1) 

    
    def test_insert_categories(self):
        Category.insert_categories()
        c = Category.query.all()
        self.assertTrue( c is not None) 

    '''
    def test_set_category_or(self):
        group = Group(groupname = 'Phil', founder=2, category = GroupDoes.NECESSARY)
        group.set(GroupDoes.MEETING)
        group.set(GroupDoes.REGISTRATION)
        #print('has_meetings: ', group.has_meetings())
        self.assertTrue(group.has_meetings())
        self.assertTrue(group.requires_registration())
        self.assertTrue(group.requires_registration())
    '''