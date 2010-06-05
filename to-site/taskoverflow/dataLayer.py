import models
import settings

def memoize(key, time=60):
    """Decorator to memoize functions using memcache."""
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            data = memcache.get(key)
            if data is not None:
                return data
            data = fxn(*args, **kwargs)
            memcache.set(key, data, time)
            return data
        return wrapper if not settings.DEBUG else fxn
    return decorator


class DataLayer():
    def GetTaskTypes(self):
        #TODO: memcache
        types = models.TaskType().all().fetch(1000)
        return types
    
    def GetTaskTemplate(self, template_key):
        #TODO: memcache
        types = models.TaskType().get(template_key)
        return types   
        
    @memoize('tasks')   
    def GetTasks(self):
        #TODO: memcache
        #TODO: sort
        tasks = models.Task().all().fetch(1000)
        return tasks
    
    def CreateUser(self,Name,DateOfBirth,UserName):
        newUser = models.User()
        newUser.Name = Name
        newUser.DateOfBirth = DateOfBirth
        newUser.UserName = UserName
        newUser.Put()
        
        #TODO: flush memcache
       
    def CreateTask(self,title,expiration,estimatedTime,taskType,points=0):
        newTask = models.Task()
        task.title = title
        task.expiration = expiration
        task.estimatedTime = estimatedTime
        task.points = points
        task.TaskType = GetTaskType(taskType)
        task.put()
        
        #TODO: flush memcache
    
    def GetTaskType(id):
        #TODO: add memcache
        return models.TaskType.get_by_id(id)