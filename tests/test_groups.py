import sys
import unittest
import time
from datetime import datetime, timezone
from app import create_app, db
from app.models import Group, Category, User, Comment


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
        founder = User(email='puss@warm.mews', name='cooking_fat', password='cat')
        db.session.add( category )
        db.session.add(founder)
        #db.session.commit()
        group = Group(groupname = 'Phil', category = category, founder = founder)
        self.assertTrue(group.groupname == 'Phil')
        self.assertTrue(group.category == category) 
        print('category: {}, founder: {}'.format( category, founder ))
        self.assertTrue(group.category.description == 'test category')
        self.assertTrue(group.founder.name == 'cooking_fat')

    
    def test_insert_categories(self):
        Category.insert_categories()
        c = Category.query.first()
        self.assertTrue( c is not None) 

    
    def test_group_has_meetings(self):
        Category.insert_categories()
        category = Category.query.first()
        founder = User(email='puss@warm.mews', name='cooking_fat', password='cat')
        group = Group(groupname = 'Phil', founder = founder, category = category)
        db.session.add( founder )
        self.assertTrue('Online Only' in group.category.description )
        self.assertFalse('meet' in group.category.description )

    '''
    def test_topic_group(self):
        Category.insert_categories()
        category = Category.query.first()
        founder = User(email='puss@warm.mews', name='cooking_fat', password='cat')
        db.session.add( founder )
        group = Group(groupname = 'Phil', founder = founder, category = category)
        db.session.add( group )
        comment = Comment(content='Eh?', topic=topic )
    '''