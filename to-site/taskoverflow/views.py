# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def task_view(request, task_id):
    return HttpResponse("Viewing task")
    
@login_required
def task_new(request, task_id):
    return HttpResponse("Creating Views")
