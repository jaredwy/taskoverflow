import datetime
from google.appengine.ext import db
from google.appengine.api import users

class TaskState(db.Model):
    state = db.StringProperty(required=True, choices=set(["Working", 
    "Completed", "Listed","Review"]))

class TaskMetaData(db.Expando):
    name = db.StringProperty()
    Task = db.ReferenceProperty(Task,
                                    collection_name='taskMetaData')

class TaskTemplate(db.Model):
    template = db.StringProperty()
    
class TaskType(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()
    TaskTemplate = TaskTemplate()
    
class Task(db.Model):
    expiration = db.DateTimeProperty()
    completed = db.DateTimeProperty()
    estimatedTime = db.TimeProperty()
    ID = db.IntegerProperty()
    points = db.IntegerProperty()
    taskType = TaskType()
    taskState = TaskState()
