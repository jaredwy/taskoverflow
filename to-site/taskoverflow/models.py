from appengine_django.models import BaseModel
from google.appengine.ext import db


# Create your models here.
class TaskTemplate(db.Model):
    template = db.StringProperty()
    
class TaskType(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()
    TaskTemplate = db.ReferenceProperty(TaskTemplate)

class TaskState(db.Model):
    state = db.StringProperty(required=True, choices=set(["Working", 
    "Completed", "Listed","Review"]),default="Listed")

class TaskMetaData(db.Expando):
    pass


class Task(db.Model):
    title = db.StringProperty()
    description = db.TextProperty()
    expiration = db.DateTimeProperty()
    points = db.IntegerProperty()
    estimated_time = db.TimeProperty()
    task_type = db.ReferenceProperty(TaskType)
    completed = db.DateTimeProperty(auto_now_add=True)
    task_state =  db.ReferenceProperty(TaskState)
    task_meta_data = db.ReferenceProperty(TaskMetaData)


class User(db.Model):
    Name = db.StringProperty()
    DateOfBirth = db.DateProperty()
    UserName = db.StringProperty()

class UserTraits(db.Model):
    User = db.ReferenceProperty(User, collection_name='UserTraits')
    Points = db.IntegerProperty()
    Trait = db.ReferenceProperty(TaskType)

class UserTasks(db.Model):
    Own = db.BooleanProperty()
    User = db.ReferenceProperty(User,collection_name='UserTasks')


