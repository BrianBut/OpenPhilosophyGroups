import unittest
from datetime import datetime, time
from app import create_app, db
from app.models import User, AnonymousUser, Topic, Role, Group, Comment


class TopicModelTestCase(unittest.TestCase):
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

    def test_title(self):
        t = Topic(title="Test Topic")
        self.assertTrue(t.title is not None)

    def test_creation_datetime(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.commit()
        t2 = Topic.query.first()
        #print("t.creation_datetime: {}".format(t2.creation_datetime))
        self.assertTrue(t.creation_datetime is not None)

    def test_discussion_datetime(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.flush()
        #print("t.discussion_datetime: {}".format(t.discussion_datetime))
        self.assertTrue(t.discussion_datetime == datetime.min)

    def test_discussion_timediff(self):
        t = Topic(title="Test Topic")
        db.session.add(t)
        db.session.flush()
        timediff_in_seconds = ( t.discussion_datetime - datetime.min ).total_seconds()
        #print( 'timediff', timediff_in_seconds )
        assert isinstance(timediff_in_seconds, float)
        self.assertTrue(timediff_in_seconds < 0.5)

    def test_published_default_is_proposed(self):
        t = Topic(title="Test Topic")
        t.published = 0
        db.session.add(t)
        db.session.commit()
        t2 = Topic.query.first()
        #print('discussion_venue; {}, published: {}'.format( t2.discussion_venue(), t2.published ))
        self.assertTrue( int(t2.published) == 0 )
        self.assertTrue( t.discussion_venue() == 'proposed' )
        self.assertTrue( t.discussion_datetime == datetime.min )

    def test_topic_is_online(self):
        t = Topic(title="Test Topic")
        t.published = 1
        db.session.add(t)
        db.session.commit()
        t2 = Topic.query.first()
        self.assertTrue(t2.discussion_venue() == 'online')
    
    def test_topic_author(self):
        author = User(email='puss@warm.mews', name='cooking_fat', password='cat')
        db.session.add(author)
        t = Topic(title="Test Topic2", author=author)
        self.assertTrue( t.author.name == 'cooking_fat' )

    def test_topic_group(self):
        founder = User(email='puss@warm.mews', name='cooking_fat', password='cat')
        topic = Topic(title='Test Topic2')
        group = Group( groupname='Testing Topic Group', founder=founder )
        self.assertTrue( group.groupname == 'Testing Topic Group')
        self.assertTrue( group.founder.name == 'cooking_fat')

    def test_comment_creation_datetime(self):
        t = Comment(content="Test Topic")
        db.session.add(t)
        db.session.commit()
        t2 = Comment.query.first()
        #print("t.creation_datetime: {}".format(t2.creation_datetime))
        self.assertTrue(t2.creation_datetime is not None)

    def test_comment_author(self):
        author = User(email='me@my.home', password='cheese', name='Brian')
        db.session.add( author )
        comment = Comment(content='Still Testing', author=author)
        db.session.add(comment)
        print( comment.author.name )
        self.assertTrue( comment.author.name == 'Brian')
