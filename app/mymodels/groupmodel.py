from app import db

class GroupDoes:
    INFO = 1
    TODO = 2
    ONLINE = 4
    MEETING = 8
    REGISTRATION = 16 # Only member who are on the register can see these groups
    NECESSARY = 32


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    groupname = db.Column(db.String(128), unique=True, nullable=False )
    founder = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Integer, nullable=False)

    @staticmethod
    def insert_default_group():
        group = Group(groupname='Open Philosphy Groups', founder=1, category=GroupDoes.INFO)
        db.session.add( group )
        db.session.commit()
    
    def set(self, gd):
        d = int(gd)
        category1 = self.category
        self.category = int(self.category) | d 
        print('D: {}, category: {}, int(self.category) or d {}'.format(d, category1, int(self.category) or d))

    def is_info(self):
        if GroupDoes.INFO & self.category:
            return True

    def is_todo(self):
        if GroupDoes.TODO & self.category:
            return True

    def is_necessary(self):
        if GroupDoes.NECESSARY & self.category:
            return True

    def has_meetings(self):
        if GroupDoes.MEETING & self.category:
            return True
        return False

    # ie contribute or comment
    def requires_registration(self):
        if GroupDoes.REGISTRATION & self.category:
            return True

    #def is_necessary(self):
    #    return self.bit_test()



    
    
