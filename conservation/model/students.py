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
        return {"_uuid": self._uuid, "username": self._username, "_uuaid": self._uuaid, "points": self._points, "levels": self._levels}
    
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None


    def read(self):
        return {
            "uuid": self._uuid,
            "username": self._username,
            "uuaid": self._uuaid,
            "points": self._points,
            "levels": self._levels
        }

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
    test_accounts = [Student(3, "test_user", 2, 34, 0), Student(4, "Eris29", 2, 0 ,5)]
    for account in test_accounts:
        try:
            user_object = account.create()
            print(f"Created new student {user_object.username}")
            db.session.add(account)
            db.session.commit()
        except:
            print(f"Operation with student has failed") 