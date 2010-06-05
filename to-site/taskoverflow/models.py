from appengine_django.models import BaseModel
from google.appengine.ext import db

# Create your models here.
class TaskTemplate(db.Model):
    template = db.StringProperty()
    
class TaskType(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()
    TaskTemplate = TaskTemplate()

class TaskState(db.Model):
    state = db.StringProperty(required=True, choices=set(["Working", 
    "Completed", "Listed","Review"]),default="Listed")

class Task(db.Model):
    title = db.StringProperty()
    expiration = db.DateTimeProperty()
    completed = db.DateTimeProperty()
    estimatedTime = db.TimeProperty()
    ID = db.IntegerProperty()
    points = db.IntegerProperty()
    taskType = TaskType()
    taskState = TaskState()

class TaskMetaData(db.Expando):
    UserID = db.IntegerProperty()
    Task = db.ReferenceProperty(Task,
                                    collection_name='taskMetaData')

class User(db.Model):
    ID = db.IntegerProperty()
    Name = db.StringProperty()
    DateOfBirth = db.DateProperty()
    UserName = db.StringProperty()


class UserTraits(db.Model):
    User = db.ReferenceProperty(User, collection_name='UserTraits')
    Points = db.IntegerProperty()
    Trait = TaskType()

class UserTasks(db.Model):
    Own = db.BooleanProperty()
    User = db.ReferenceProperty(User,collection_name='UserTasks')

