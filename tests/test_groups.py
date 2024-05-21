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
        category = Category(description='test category')
        group = Group(groupname = 'Phil', category = category)
        self.assertTrue(group.groupname == 'Phil', group.category == category) 
        self.assertTrue(group.category.description == 'test category')

    
    def test_insert_categories(self):
        Category.insert_categories()
        c = Category.query.all()
        self.assertTrue( c is not None) 

    def test_group_has_meetings(self):
        Category.insert_categories()
        category = Category.query.first()
        group = Group(groupname = 'Phil', category = category)
        self.assertTrue('Online Only' in group.category.description )
        self.assertFalse('meet' in group.category.description )
        