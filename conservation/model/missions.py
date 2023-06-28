from sqlalchemy import Column, Integer, Text
from sqlalchemy.exc import IntegrityError
from conservation.helpers import cast_int
from conservation import db


class Missions(db.Model):
    __tablename__ = 'event_missions'
    id = Column(Integer, primary_key=True)
    _name = Column(Text, nullable=False)
    _value = Column(Integer, nullable=True)
    _visibility = Column(Integer, nullable=False)                 # -1 = broadcast = all users can see, else, store csv of advisors who assigned it
    _description = Column(Integer, nullable=True)
    _time = Column(Integer, nullable=True)                       # Store as Unix Time
    _location = Column(Text, nullable=True)
    
    def __init__(self, name, value, visibility, description, time, location):
        self._name = name
        self._value = cast_int(value)
        self._visibility = cast_int(visibility)
        self._description = description
        self._time = cast_int(time)
        self._location = location
    
    def __repr__(self):
        return "<mission(id='%s', name='%s', value='%s', visibility='%s', description='%s', time='%s', location='%s')>" % (
            self.id,
            self._name,
            self._value,
            self._visibility,
            self._description,
            self._time,
            self._location
        )
    
    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        self.name = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def to_dict(self):
        return {"name": self._name, "value": self._value, "visibility": self._visibility, "description": self._description, "time": self._time, "location": self._location}
    
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
            "id": self.id, 
            "name": self._name, 
            "value": self._value, 
            "visibility": self._visibility, 
            "description": self._description, 
            "time": self._time, 
            "location": self._location
        }

    def update(self, name="", value="", visibility="", description ="", time="", location=""):
        if len(name) >= 3:
            self._name = name
        if value:
            self._value = cast_int(value)
        if visibility:
            self._visibility = cast_int(visibility)
        if description:
            self._description = description
        if time:
            self._time = cast_int(time)
        if location:
            self._location = location
        db.session.commit()
        return self.read()


    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def init_missions():
    test_missions = [Missions("Nepal", 5000, -1, "Alleviate education for children", -1, "Nepal")]
    for mission in test_missions:
        try:
            mission_object = mission.create()
            print(f"Created new mission {mission_object.name}")
            db.session.add(mission)
            db.session.commit()
        except:
            print(f"Operation with mission has failed")