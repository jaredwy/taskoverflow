# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

def task_view(request, task_id):
    return render_to_response('task_view.html', {},
                               context_instance=RequestContext(request))
    
def task_new(request):
    task_templates = [{'id': 'languagetranslate', 'name': 'Language Translation'},
                      {'id': 'mapfix', 'name': 'Map Digitize'}]
    return render_to_response('task_new.html', {'task_templates': task_templates},
                               context_instance=RequestContext(request))

def tasktemplate(request, tasktemplate_id):
    task_fields =  [
     {"label": "From",
      "name": "fromlanguage",
      "value": "",
      "type": "input"},
     {"label": "To",
      "name": "tolanguage",
      "value": ["spanish", "english"],
      "type": "dropdown"},]
    return render_to_response('taskfield_include.html', {'task_fields': task_fields},
                               context_instance=RequestContext(request))
 
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
