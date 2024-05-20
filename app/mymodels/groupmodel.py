from app import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    groups = db.relationship('Group', backref='category', lazy='dynamic')

    # Return a list of choices suitable for use in a select field
   # @staticmethod():
    #def choices():
    #    choices = Category.query.filter( Category.description != None).description.all()

    @staticmethod
    def insert_categories():
        catstrings = 'Online Only (Anyone can contribute),Online and has meetings (Anyone can contribute),Online Only (Membership Required),Online and has meetings (Membership Required),,,,,,,Necessary,Info,Todo'
        categories = catstrings.split(',')
        assert( len(categories) == 13)
        for i, c in enumerate(categories):
            category = Category.query.filter_by(id=i).first()
            if category is None:
                cat = Category( description = c )
                db.session.add( cat )
        db.session.commit()

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(128), unique=True, nullable=False )
    founder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    topics = db.relationship('Topic', backref='creator', lazy='dynamic')


    @staticmethod
    def insert_default_group():
        group = Group(groupname='Open Philosphy Groups', category_id=10 )
        db.session.add( group )
        db.session.commit()
    



    
    
