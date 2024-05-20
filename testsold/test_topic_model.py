import unittest
from datetime import datetime, time
from app import create_app, db
from app.models import User, AnonymousUser, Topic, Role


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
    
    def test_topic_dump_author_id(self):
        title = "Testing Title"
        summary = "Summary blurb"
        content = "More blurb"
        #creation_datetime = db.Column(db.DateTime, default=datetime.utcnow)
        #discussion_datetime = db.Column(db.DateTime, default=datetime.min)
        #published = db.Column(db.Boolean, default=False)
        r=Role.query.filter_by(name='Guest').first()
        db.session.add( r )
        db.session.flush()
        author=User(email='puss@warm.mews', name='Fat_Cat', password='phrrrr', role=r)
        db.session.add(author)
        db.session.commit() # needed for author.id
        self.assertTrue(author.id==1) # not a string
        t=Topic(title=title, summary=summary, content=content, author_id=author.id)
        db.session.add( r )
        db.session.add( author )
        db.session.add( t )
        db.session.commit()
        #print("dump: ",t.dump())
        self.assertTrue(t.title==title)
        self.assertTrue(t.summary==summary)
        self.assertTrue(t.content==content)

    #def test_markdown(self):

    def test_admin_topic_author_full_name(self):
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='johnsmith@example.com', password='cat', name='Admin_Lee', role=r )
        db.session.add(u)
        db.session.flush()
        topic=Topic(title="Test Author Fullname", author_id=u.id)
        db.session.add(topic)
        db.session.commit()
        self.assertTrue( topic.author_fullname() == 'Admin Lee')
        #self.assertTrue(topic.author_fullname == 'Admin_Lee')