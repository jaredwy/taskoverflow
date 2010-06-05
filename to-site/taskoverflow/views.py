# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

def task_view(request, task_id):
    return render_to_response('task_view.html', {},
                               context_instance=RequestContext(request))
    
def task_new(request):
    return HttpResponse("Creating task")

def tasks_search(request): 
    # Extract query params, do search
    # Render into search panel
    return HttpResponse("Searching tasks")
  
def tasks_recent(request):
    # Extract recent query params (like user), do db query
    # Render into recent tasks widget
    tasks = [{'title': 'Translate 10 phrases'}, 
             {'title': 'Translate 20 phrases'}]
    return render_to_response('tasks_recent.html', {'tasks': tasks},
                               context_instance=RequestContext(request))
    
def user_view(request, user_id):
    # Get user info, render into 
    return HttpResponse("Showing user")
