# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import tzinfo, timedelta, datetime, date
import models
def task_view(request, task_id):
    return HttpResponse("Viewing task")
    
def task_new(request):
    return HttpResponse("Creating task")
    
def user_view(request, user_id):
    return HttpResponse("Showing user")

def create_data(request):
  
    create = DataCreater()
    users = create.CreateUsers()
    
    templates = create.CreateTaskTemplates()
    taskTypes = create.CreateTaskType(templates)
    traits = create.CreateUserTraits(taskTypes,users)
    
    create.CreateUserInfo(users)
    return HttpResponse("created user")




class DataCreater():
    #user creators
    def CreateUsers(self):
        usera = models.User()
        userb = models.User()

        usera.Name = "Creating User"
        userb.Name = "Cletus"

        usera.DateOfBirth = date.today()
        userb.DateOfBirth = date.today()

        usera.UserName = "Something"
        userb.UserName = "Cletus"

        return usera,userb
        
    def CreateUserInfo(self,users):
        for user in users:
            print user.Name
            
            
    def CreateUserTraits(selfe,type,users):
        print type
        users[0].put()
        users[1].put()
        traita = models.UserTraits(User=users[0],Points=10,Trait=type[0])
        traitb = models.UserTraits(User=users[1],Points=100,Trait=type[1])
        traita.put()
        traitb.put()
        return traita,traitb
        
    def CreateTaskType(self,template):
        taskTypea = models.TaskType()
        taskTypea.name = "Translate"
        taskTypea.value = "Spanish.English"
        taskTypea.TaskTemplate = template[0]
        
        taskTypeb = models.TaskType()
        taskTypeb.name = "Mapping"
        taskTypeb.value = "Find.Road"
        taskTypeb.TaskTemplate = template[1]
        taskTypeb.put()
        taskTypea.put()
        return taskTypea,taskTypeb
        
    def CreateTaskTemplates(self):
        templatea = models.TaskTemplate()
        templatea.template = '{"template":[{"translate":"","somethingelse":""}]}'
        templateb = models.TaskTemplate()
        templateb.template = '{"template":[{"map":"Tenth road"}]}'
        templatea.put()
        templateb.put()
        return templatea, templateb
    
    