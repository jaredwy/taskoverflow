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
    
    def GetMetadataLabels(self):
        # TODO - replace with datastore later?
        labels = {'from_language': 'From',
                  'to_language': 'To',
                  'location': 'Location'}
        return labels
        
    def GetTaskTemplate(self, tasktype_id):
        task = models.TaskType().get_by_id(tasktype_id)
        return task.TaskTemplate.template 
        
    
    #@memoize('tasks')   
    def GetTasks(self):
        #TODO: sort
        tasks = models.Task().all().fetch(1000)
        return tasks
        
    #@memoize('tasks')   
    def GetTask(self, task_id):
        tasks = models.Task().get_by_id(task_id)
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
        newUser.put()
        
    def GetTaskTemplate(self,templateid):
        return models.TaskTemplate().get_by_id(templateid)
       
    def CreateTask(self,title,expiration,estimatedTime,taskType,description='',points=0):
        task = models.Task()
        task.title = title
        task.expiration = expiration
        task.estimatedTime = estimatedTime
        task.points = points
        task.description = description
        task.TaskType = self.GetTaskType(taskType)
        task.put()
        return task.key().id()
        
    #@memoize('tasktypes')  
    def GetTaskType(self, id):
        #TODO: add memcache
        return models.TaskType.get_by_id(id)