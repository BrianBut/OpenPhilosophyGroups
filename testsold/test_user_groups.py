import sys
import unittest
import time
from datetime import datetime, timezone
from app import create_app, db
from app.models import User, AnonymousUser, Role, Group


class UserModelTestCase(unittest.TestCase):
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

    def test_groups_not_null(self):
        user = User(password='cat', groups=7)
        #print('groups: ', user.groups )
        self.assertTrue(user.groups) is str

    def test_mygrouplist_type_is_list(self):
        user = User(password='cat', groups=5)
        #print( 'mygrouplist: {}'.format( user.mygrouplist() ))
        self.assertTrue( type(user.mygrouplist()) is list )

    def test_addgroup(self):
        user = User(name='cooking_fat', password='cat', groups=7 )
        user.addgroup(3)
        #print('groups: ',user.groups)
        user.addgroup(4)
        #print('groups: ',user.groups)
        #print( 'mygroups: {}'.format( user.mygrouplist() ))
        self.assertTrue( type(user.mygrouplist()) == list )

    def test_addgroup_ignores_duplicates(self):
        user = User(name='cooking_fat', password='cat', groups=7 )
        user.addgroup(3)
        user.addgroup(3)
        #print('mygrouplist: {}'.format(user.mygrouplist()))
        self.assertTrue( len(user.mygrouplist()) == 2)

    def test_removegroup(self):
        user = User(name='cooking_fat', password='cat', groups=7 )
        user.addgroup(3)
        #print('groups: ',user.groups)
        user.removegroup(7)
        #print( 'mygroups: {}'.format( user.mygrouplist() ))
        self.assertTrue( type(user.mygrouplist()) is list)
        self.assertTrue(len(user.mygrouplist()) == 1)

    '''
    def test_mygroupchoices(self):
        gp = Group(groupname='Brians Group')
        db.session.add(gp)
        gp1 = Group(groupname='Johns Group')
        db.session.add(gp1)
        db.session.commit()
        user = User(name='cooking_fat', password='cat', groups=1 )
        grs = Group.query.all()
        for grp in grs:
            user.addgroup(grp.id)
        print( 'mygroupchoices: ',user.mygroupchoices() )
    '''  