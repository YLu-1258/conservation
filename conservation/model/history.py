from sqlalchemy import Column, Integer, Text
from sqlalchemy.exc import IntegrityError
from conservation.helpers import cast_int
from conservation import db


class History(db.Model):
    __tablename__ = 'user_history'
    id = Column(Integer, primary_key=True)
    _uuid = db.Column(Integer, db.ForeignKey('user_info.id'), nullable=False)
    _name = Column(Text, nullable=False)
    _value = Column(Integer, nullable=True)
    _visibility = Column(Integer, nullable=False)                 
    _description = Column(Integer, nullable=True)
    _time = Column(Integer, nullable=True)                       #
    _location = Column(Text, nullable=True)
    _progress = Column(Integer, nullable=False)
    
    def __init__(self, uuid, name, value, visibility, description, time, location, progress):
        self._uuid = uuid
        self._name = name
        self._value = cast_int(value)
        self._visibility = cast_int(visibility)
        self._description = description
        self._time = cast_int(time)
        self._location = location
        self._progress = progress
    
    def __repr__(self):
        return "<history(id='%s', uuid='%s', name='%s', value='%s', visibility='%s', description='%s', time='%s', location='%s', progress='%s')>" % (
            self.id,
            self._uuid,
            self._name,
            self._value,
            self._visibility,
            self._description,
            self._time,
            self._location,
            self._progress
        )
    
    @property
    def uuid(self):
        return self._uuid
    
    @uuid.setter
    def uuid(self, value):
        self._uuid = value
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

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

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        self._progress = value

    def to_dict(self):
        return {"id": self.id,
                "uuid": self.uuid,
                "name": self._name, 
                "value": self._value, 
                "visibility": self._visibility, 
                "description": self._description, 
                "time": self._time, 
                "location": self._location,
                "progress": self._progress}
    
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def update(self, uuid="", name="", value="", visibility="", description ="", time="", location="", progress=""):
        if uuid:
            self._uuid = cast_int(uuid)
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
    
def init_entrys():
    test_history = [
        History(4, "Nepal", 5000, -1, "Alleviate education for children", -1, "Nepal", 1),
        History(4, "Hunan", 1000, 2, "Support community development initiatives", -1, "China", 0),
        History(4, "MiraMesa", 2000, 2, "Community development and improvement", 1688743257, "San Diego", 1),
        History(4, "India", 3000, 1, "Support healthcare for rural communities", -1, "India", 0),
        History(4, "Tokyo", 4000, 0, "Upgrade transportation infrastructure", -1, "Japan", 1),
        History(4, "Sydney", 1500, 2, "Enhance environmental conservation efforts", -1, "Australia", 0),
        History(4, "New York", 2500, 2, "Provide assistance to homeless shelters", -1, "United States", 1),
        History(4, "London", 3500, 1, "Revitalize local parks and green spaces", -1, "United Kingdom", 0),
        History(4, "Rio de Janeiro", 7500, 2, "Develop sustainable tourism initiatives", -1, "Brazil", 1),
        History(4, "Seoul", 6200, 0, "Expand cultural exchange programs", -1, "South Korea", 0),
        History(4, "Paris", 3000, 1, "Preserve historical landmarks and monuments", -1, "France", 1),
        History(4, "Moscow", 4500, 2, "Support arts and cultural events", -1, "Russia", 0),
        History(4, "Berlin", 5200, 1, "Improve access to affordable housing", -1, "Germany", 1),
        History(4, "Cairo", 4000, 2, "Promote renewable energy adoption", -1, "Egypt", 0),
        History(4, "Mexico City", 6800, 0, "Enhance public transportation systems", -1, "Mexico", 1),
        History(4, "Buenos Aires", 5700, 1, "Invest in entrepreneurship and small businesses", -1, "Argentina", 0),
        History(4, "Amsterdam", 4800, 2, "Create sustainable urban mobility solutions", -1, "Netherlands", 1),
        History(4, "Toronto", 8000, 1, "Empower marginalized communities", -1, "Canada", 0),
        History(4, "Singapore", 9200, 2, "Enhance digital infrastructure and connectivity", -1, "Singapore", 1),
        History(4, "Mumbai", 5700, 1, "Improve public healthcare services", -1, "India", 0)
    ]
    for entry in test_history:
        try:
            entry_object = entry.create()
            print(f"Created new history entry {entry_object.name}")
            db.session.add(entry)
            db.session.commit()
        except:
            print(f"Operation with history entry has failed")