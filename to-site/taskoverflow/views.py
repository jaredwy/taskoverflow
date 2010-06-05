# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import models
def task_view(request, task_id):
    return HttpResponse("Viewing task")
    
def task_new(request):
    return HttpResponse("Creating task" + newTask.ID)
    
def user_view(request, user_id):
    return HttpResponse("Showing user")
