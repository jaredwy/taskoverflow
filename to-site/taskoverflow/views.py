# Create your views here.
import logging

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import tzinfo, timedelta, datetime, date
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson

import models
import dataLayer

def task_view(request, task_id):
    data = dataLayer.DataLayer()
    task = data.GetTask(int(task_id))
    return render_to_response('task_view.html', {'task': task},
                               context_instance=RequestContext(request))
    
def task_new(request):
    data = dataLayer.DataLayer()
    templates = data.GetTaskTypes()
    return render_to_response('task_new.html', {'task_templates': templates},
                               context_instance=RequestContext(request))



def tasktemplate(request, tasktemplate_id):
    data = dataLayer.DataLayer()
    logging.info(tasktemplate_id)
    template = data.GetTaskTemplate(int(tasktemplate_id))
    logging.info(template)
    task_fields = simplejson.loads(template)
    return render_to_response('taskfield_include.html', {'task_fields': task_fields},
                               context_instance=RequestContext(request))
 
def tasks_search(request): 
    data = dataLayer.DataLayer()
    templates = data.GetTaskTypes()
    # Extract query params, do search
    # Render into search panel
    return render_to_response('tasks_search.html',{'task_types' : templates},
                               context_instance=RequestContext(request))
  
def tasks_recent(request):
    # Extract recent query params (like user), do db query
    # Render into recent tasks widget
    data = dataLayer.DataLayer()
    tasks = data.GetTasks()
    logging.info(tasks)
    return render_to_response('tasks_recent.html', {'tasks': tasks},
                               context_instance=RequestContext(request))
    
def user_view(request, user_id):
    # Get user info, render into 
    return HttpResponse("Showing user")

def create_data(request):
  
    create = DataCreater()
    users = create.CreateUsers()
    
    templates = create.CreateTaskTemplates()
    taskTypes = create.CreateTaskType(templates)
    traits = create.CreateUserTraits(taskTypes,users)
    logging.info("Created a task with id" + str(create.CreateTasks(taskTypes)))
    #create.CreateUserInfo(users)
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
            
    def CreateTasks(self,types):
        taska = models.Task()
        taska.title = "Dig a hole"
        taska.points = 10
        taska.taskType = types[0]
        taska.put()
        return taska.key().id()
     
    def CreateUserTraits(self,type,users):
        users[0].put()
        users[1].put()
        traita = models.UserTraits(User=users[0],Points=10,Trait=type[0])
        traitb = models.UserTraits(User=users[1],Points=100,Trait=type[1])
        traita.put()
        traitb.put()
        return traita,traitb
        
    def CreateTaskType(self,templates):
        taskTypea = models.TaskType()
        taskTypea.name = "Translate"
        taskTypea.value = "Spanish.English"
        taskTypea.TaskTemplate = templates[0]
        
        taskTypeb = models.TaskType()
        taskTypeb.name = "Mapping"
        taskTypeb.value = "Find.Road"
        taskTypeb.TaskTemplate = templates[1]
        taskTypeb.put()
        taskTypea.put()
        return taskTypea,taskTypeb
        
    def CreateTaskTemplates(self):
        templatea = models.TaskTemplate()
        templatea_fields = [
         {"label": "From",
          "name": "fromlanguage",
          "value": ["Spanish", "English", "Portuguese"],
          "type": "dropdown"},
         {"label": "To",
          "name": "tolanguage",
          "value": ["Spanish", "English", "Portuguese"],
          "type": "dropdown"
          }];
        templatea.template = simplejson.dumps(templatea_fields)
        templateb = models.TaskTemplate()
        templateb_fields = [
         {"label": "Location",
          "name": "location",
          "value": "",
          "type": "input"}
          ];
        templateb.template = simplejson.dumps(templateb_fields)
        templatea.put()
        templateb.put()
        return templatea, templateb
    
    
