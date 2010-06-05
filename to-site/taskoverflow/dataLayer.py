import models

class DataLayer():
    def GetTaskTypes(self):
        #TODO: memcache
        types = models.TaskType().all().fetch(1000)
        return types
        
    def GetTasks(self):
        #TODO: memcache
        #TODO: sort
        types = models.Tasks().all().fetch(1000)
        return types
    
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