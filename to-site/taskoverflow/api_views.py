"""
Contains the API views for the 
"""

import sys
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
# from django.core.validators

# TODO: move this into a library out of the views (maybe??)
def apigen_validate(request, instructions):
    validation_errors = {}
    
    # iterate through the instructions and check to see if everything stacks up
    for fname, finst in instructions.iteritems():
        print >> sys.stderr, "checking validity of field: %s\n" % fname,
        
        # if the field is required and no data is supplied then add a validation error
        if (finst['required'] and (not request.POST.__contains__(fname))):
            validation_errors[fname] = "Field is required"
        # if we get past the requiredness check, let run the specified validators
            
    return validation_errors
    
# TODO: move this to the module aswell
def render_validation_error(validation_errors):
    # TODO: serialize this to JSON
    return HttpResponse(validation_errors)


"""
Task update methods

TODO: add login decorator
"""
def task_update(request, key):
    if (request.method == 'POST'):
        print >> sys.stderr, "GOT POSTED VALUES\n",
    

    for k, v in request.POST.iteritems():
        print >> sys.stderr, "%(key)s: %(value)s\n" % {'key': k, 'value': v},

    return HttpResponse("TASK UPDATE API")
    
"""
ENDPOINT:
/api/task/create

DESCRIPTION:
Used to create a new task in the task DB

METHODS: 
POST

POSTDATA:
task_name - required - text
task_expiration - required - date (format: yyyy-mm-dd hh:mi:ss)
task_est - required - text 
task_typeid - required - valid task id
task_points - optional - integer point value for the task
"""
def task_create(request):
    
    # define my treatment of parameters
    param_instructions = {
        'task_name': {
            'required': True,
        },
        'task_expiration': {
            'required': True,
            'validation': ['isValidANSIDatetime'],
        },
        'task_est': {
            'required': True,
        },
        'task_typeid': {
            'required': True,
            # ADD CUSTOM VALIDATION TO CHECK FOR TASK TYPE EXISTANCE
        },
        'task_points': {
            'required': False,
            'validation': ['isInteger'],
        }}

    # ask for some validation
    validation_errors = apigen_validate(request, param_instructions)
    
    # if we have validation errors then wrap a validaton error response
    if (validation_errors):
        return render_validation_error(validation_errors)