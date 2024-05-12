import sys
import unittest
import time
from datetime import datetime, timezone
from app import create_app, db
from app.models import Group, Category, GroupDoes


class CategoryTestCase(unittest.TestCase):
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
        self.assertTrue(group.groupname == 'Phil') 

    def test_default_category(self):
        c = Category()
        db.session.add(c)
        db.session.commit()
        c = Category.query.first()
        #print('c: {}'.format(c))
        self.assertTrue(c.activities == GroupDoes.ONLINE)

    def test_add_and_remove_category(self):
        c = Category()
        db.session.add(c)
        db.session.commit()
        c = Category.query.first()
        c.add_activity( GroupDoes.MEETING )
        self.assertTrue( c.activities == (GroupDoes.ONLINE | GroupDoes.MEETING ))
        c.remove_activity(GroupDoes.ONLINE)
        print( 'Activity: ', c.activities)
        self.assertTrue( c.activities == int( GroupDoes.MEETING ))

    '''
    def test_category_category(self):
        category = Category(activities=1)
        self.assertTrue(category.activities == 1)
        db.session.add(category)
        db.session.commit()
        c = Category.query.first()
        print('c: {}'.format(c))
        self.assertTrue(c.activities == 1)

    def test_category_default_category(self):
        category = Category()
        db.session.add(category)
        db.session.commit()
        c = Category.query.first()
        print('c: {}'.format(c))
        self.assertTrue(c.activities == 4)
    '''