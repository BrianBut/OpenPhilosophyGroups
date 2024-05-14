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
        group = Group(groupname = 'Phil', founder = 1)
        #print('groupname, ',group.groupname)
        self.assertTrue(group.groupname == 'Phil', group.category == GroupDoes.INFO) 

    def test_info_group(self):
        group = Group(groupname = 'Phil', founder=1, category = GroupDoes.INFO)
        self.assertTrue( group.is_info() )
        self.assertFalse( group.is_online())

    def test_todo_group(self):
        group = Group(groupname = 'Phil', founder=1, category = GroupDoes.TODO)
        self.assertTrue( group.is_todo())
        self.assertFalse( group.is_info() )
        self.assertFalse( group.is_online())

    def test_set_category(self):
        group = Group(groupname = 'Phil', founder=1, category = 0)
        group.set(GroupDoes.ONLINE)
        self.assertTrue(group.category == GroupDoes.ONLINE)
        self.assertTrue(group.category == 4)

    def test_set_category_or(self):
        group = Group(groupname = 'Phil', founder=2, category = GroupDoes.ONLINE)
        group.set(GroupDoes.MEETING)
        group.set(GroupDoes.REGISTRATION)
        #print('has_meetings: ', group.has_meetings())
        self.assertTrue(group.has_meetings())
        self.assertTrue(group.is_online())
        self.assertTrue(group.requires_registration())
