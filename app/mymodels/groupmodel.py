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
    category = db.Column(db.Integer)

    @staticmethod
    def insert_default_group():
        group = Group(groupname='Open Philosphy Groups', category=GroupDoes.INFO)
        db.session.add( group )
        db.session.commit()

    def bit_test(self, bitno):
        if not self.category:
            self.category = 0
        bitstring = bin(self.category)[2:].zfill(6)
        #print('bitstring: ',bitstring)
        #print('bitno: {}, bitstring[bitno]: {}'.format( bitno, bitstring[bitno]))
        if bitstring[bitno] == '1':
            return True
        return False

    # has info only
    def is_info(self):
        return self.bit_test(5)

    def is_todo(self):
        return self.bit_test(4)

    def is_online_only(self):
        return self.bit_test(3)

    def is_has_meetings(self):
        return self.bit_test(2)

    # ie contribute or comment
    def requires_registration(self):
        return self.bit_test(1)

    def is_necessary(self):
        return self.bit_test()


    
    
