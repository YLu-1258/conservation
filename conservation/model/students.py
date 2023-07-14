from sqlalchemy import Column, Integer, Text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from conservation import db
from conservation.helpers import cast_int

class Student(db.Model):
    __tablename__ = 'student_info'
    id = Column(Integer, primary_key=True)
    _uuid = db.Column(Integer, db.ForeignKey('user_info.id'))
    _uuaid = Column(Integer, db.ForeignKey('user_info.id'), nullable=True)
    _username = Column(Text, unique=True, nullable=False)
    _points = Column(Integer, nullable=False)
    _levels = Column(Integer, nullable=False)
    
    def __init__(self, _uuid, username, _uuaid, points, levels):
        self._uuid = cast_int(_uuid)
        self._username = username
        self._uuaid = cast_int(_uuaid)
        self._points = cast_int(points)
        self._levels = cast_int(levels)

    def __repr__(self):
        return "<student(_uuid='%s', username='%s', _uuaid='%s', points='%s', levels='%s')>" % (
            self._uuid,
            self._username,
            self._uuaid,
            self._points,
            self._levels
        )
    
    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        self._uuid = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def uuaid(self):
        return self._uuaid

    @uuaid.setter
    def uuaid(self, value):
        self._uuaid = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, value):
        self._levels = value
    # Traditional set/getter for password updates

    def to_dict(self):
        return {"_uuid": self._uuid, 
                "username": self._username, 
                "_uuaid": self._uuaid, 
                "points": self._points, 
                "levels": self._levels}
    
    def to_dict_total_score(self):
        return {"username": self._username, 
                "points": self._levels*1000 + self._points}
    
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def update(self, username, uuaid="", points ="", levels=""):
        if len(username) >= 3:
            self._username = username
        if uuaid:
            self._uuaid = cast_int(uuaid)
        if points:
            self._points = cast_int(points)
        if levels:
            self._levels = cast_int(levels)
        db.session.commit()
        return self.read()
    
    def update_points(self, points, levels):
        self._points = points
        self._levels = levels
        db.session.commit()
        return self


    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def init_students():
    test_accounts = [
        Student(3, "test_user", 2, 34, 0),
        Student(4, "Eris29", 2, 0 ,5),
        Student(5, "Eris30", 2, 980 ,8),
        Student(6, "Eris31", 2, 290 ,13),
        Student(10, "user1", 7, 450, 7),
        Student(11, "user2", 8, 230, 12),
        Student(12, "user3", 9, 780, 9),
        Student(13, "user4", 7, 620, 15),
        Student(14, "user5", 8, 410, 6),
        Student(15, "user6", 9, 750, 2),
        Student(16, "user7", 7, 870, 14),
        Student(17, "user8", 8, 540, 3),
        Student(18, "user9", 9, 300, 18),
        Student(19, "user10", 7, 910, 5),
        Student(20, "user11", 8, 190, 11),
        Student(21, "user12", 9, 630, 17),
        Student(22, "user13", 7, 480, 4),
        Student(23, "user14", 8, 800, 10),
        Student(24, "user15", 9, 350, 16),
        Student(25, "user16", 7, 560, 8),
        Student(26, "user17", 8, 720, 13),
        Student(27, "user18", 9, 530, 1),
        Student(28, "user19", 7, 240, 20),
        Student(29, "user20", 8, 950, 0),
        Student(30, "user21", 9, 180, 19),
        Student(31, "user22", 7, 760, 4),
        Student(32, "user23", 8, 990, 10),
        Student(33, "user24", 9, 420, 16),
        Student(34, "user25", 7, 680, 8),
        Student(35, "user26", 8, 110, 13),
        Student(36, "user27", 9, 790, 1),
        Student(37, "user28", 7, 290, 20),
        Student(38, "user29", 8, 610, 0),
        Student(39, "user30", 9, 880, 19)
    ]
    for account in test_accounts:
        try:
            user_object = account.create()
            print(f"Created new student {user_object.username}")
            db.session.add(account)
            db.session.commit()
        except:
            print(f"Operation with student has failed") 