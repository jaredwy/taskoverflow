import models
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
    #@memoize(region='tasktypes')  
    def GetTaskTypes(self):
        types = models.TaskType().all().fetch(1000)
        return types
    
    
    def GetTaskTemplate(self, task_id):
        task = models.TaskType().get_by_id(task_id)
        return task.TaskTemplate.template 
        
    #@memoize('tasks')   
    def GetTasks(self):
        #TODO: sort
        tasks = models.Task().all().fetch(1000)
        return tasks
    
    #@memoize('tasks')   
    def GetTask(self,task_id):
        task = models.Task().get_by_id(task_id)
        return task
    
    def CreateUser(self,Name,DateOfBirth,UserName):
        newUser = models.User()
        newUser.Name = Name
        newUser.DateOfBirth = DateOfBirth
        newUser.UserName = UserName
        newUser.Put()
        
    def GetTaskTemplate(self,templateid):
        return models.TaskTemplate().get_by_id(templateid)
       
    def CreateTask(self,title,expiration,estimatedTime,taskType,points=0):
        newTask = models.Task()
        task.title = title
        task.expiration = expiration
        task.estimatedTime = estimatedTime
        task.points = points
        task.TaskType = GetTaskType(taskType)
        task.put()
        return taska.key().id()
        
    #@memoize('tasktypes')  
    def GetTaskType(id):
        #TODO: add memcache
        return models.TaskType.get_by_id(id)