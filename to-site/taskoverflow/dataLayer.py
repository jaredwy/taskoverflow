import models
import settings
import logging

def memoize(region="", time=3600):
    """Decorator to memoize functions using memcache.
       The calling function must give a memizekey named parameter
    """
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            if (not "memizekey" in kwargs):
                raise Exception("memize-d function does not send key")
            key = region + kwargs["memizekey"]
            del kwargs["memizekey"]

            data = memcache.get(key)
            if data is None or not settings.DEBUG:
                data = fxn(*args, **kwargs)
                memcache.set(key, data, time)
                logging.info("Cached with key" + key);
            else: logging.info("Cache hit");
            return data
        return wrapper
    return decorator 

class DataLayer():
    #@memoize('tasktypes')  
    def GetTaskTypes(self):
        types = models.TaskType().all().fetch(1000)
        return types
    
    
    def GetTaskTemplate(self, task_id):
        task = models.TaskType().get_by_id(task_id)
        return task.template 
        
    #@memoize('tasks')   
    def GetTasks(self):
        #TODO: sort
        tasks = models.Task().all().fetch(1000)
        return tasks
    
    
    def CreateUser(self,Name,DateOfBirth,UserName):
        newUser = models.User()
        newUser.Name = Name
        newUser.DateOfBirth = DateOfBirth
        newUser.UserName = UserName
        newUser.Put()

       
    def CreateTask(self,title,expiration,estimatedTime,taskType,points=0):
        newTask = models.Task()
        task.title = title
        task.expiration = expiration
        task.estimatedTime = estimatedTime
        task.points = points
        task.TaskType = GetTaskType(taskType)
        task.put()
        
    #@memoize('tasktypes')  
    def GetTaskType(id):
        #TODO: add memcache
        return models.TaskType.get_by_id(id)