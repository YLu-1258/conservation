from sqlalchemy import Column, Integer, Text
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from backend import db
from backend.helpers import cast_int


class User(db.Model):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    _username = Column(Text, unique=True, nullable=False)
    _password = Column(Text, nullable=False)
    _role = Column(Integer, nullable=False)                 # 0 = Administrator, 1 = Advisor, 2 = User
    
    def __init__(self, username, password, role):
        self._username = username
        self.set_password(password)
        self._role = cast_int(role)
    
    def __repr__(self):
        return "<user(username='%s', role='%s')>" % (
            self._username,
            self._role
        )

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    # Traditional set/getter for password updates
    def set_password(self, password):
        self._password = generate_password_hash(password, method='sha512')
      
    def is_password(self, password):
        result = check_password_hash(self._password, password)
        if result:
            return True
        else:
            return False

    def to_dict(self):
        return {"uuid": self.id, "username": self._username, "role": self._role}
    
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
            "uuid": self.id,
            "username": self._username,
            "role": self._role
        }

    def update(self, username="", password="", role=""):
        role = cast_int(role)
        if len(username) >= 3:
            self._username = username
        if len(password) >= 8:
            self.set_password(password)
        if role and role >= 0 and role <= 2:
            self._role = role
        db.session.commit()
        return self.read()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    
def init_accounts():
    test_accounts = [User("test_admin", "test_admin1234", 0), User("test_advisor", "test_advisor1234", 1), User("test_user", "test_user1234", 2), User("Eris29", "Aevus!", 2)]
    for account in test_accounts:
        try:
            user_object = account.create()
            print(f"Created new user {user_object.username}")
            db.session.add(account)
            db.session.commit()
        except:
            print(f"Operation with user has failed, perhaps dupilicate entry?")