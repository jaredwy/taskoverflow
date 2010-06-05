"""
Contains the API views for the 
"""
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

"""
Task update methods

TODO: add login decorator
"""
def task_update(request, key):
    print request.POST
    return HttpResponse("TASK UPDATE API")