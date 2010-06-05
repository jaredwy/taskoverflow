import datetime
import Tasks
from google.appengine.ext import db
from google.appengine.api import users


class User(db.Model):
    ID = db.IntegerProperty()
    Name = db.StringProperty()
    DateOfBirth = db.DateProperty()
    Status = 
    
    
class UserTraits(db.Model):
    User = db.ReferenceProperty(User, collection_name='UserTraits')
    Points = db.IntegerProperty()
    Trait = TaskType()
 
class UserTasks(db.Model):
    Own = db.BooleanProperty()
    User = db.ReferenceProperty(User,collection_name='UserTasks')
    
