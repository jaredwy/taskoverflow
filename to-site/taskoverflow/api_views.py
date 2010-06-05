"""
Contains the API views for the 
"""

import sys
import logging
from validator import Validator, ValidateError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson

class APIError(object):
    errorType = None
    params = {}
    
    def setParam(self, keyname, value = None):
        self.params[keyname] = value
    
    def __json__(self):
        json_dict = { 'errorType': self.errorType }
        
        # iterate through the parameters and push them in to the dict
        for k, v in self.params.iteritems():
            json_dict[k] = v
            
        return json_dict
        
class APIValidationError(APIError):
    target = None
    
    def __init__(self, message, target):
        self.errorType = "validation"
        self.setParam('message', message)
        self.setParam('target', target)

# TODO: move this into a library out of the views (maybe??)
def apigen_validate(request, instructions, errors):
    # define the validated field values
    validated_fieldvalues = {}
    
    # create the validator 
    vinst = Validator()
    
    # iterate through the instructions and check to see if everything stacks up
    for fname, finst in instructions.iteritems():
        logging.info("checking validity of field: %s\n" % fname)
        
        # get the field value
        field_value = None
        if request.POST.__contains__(fname):
            field_value = request.POST[fname]
        
        # if the field is required and no data is supplied then add a validation error
        if finst['required'] and (not field_value):
            errors.append(APIValidationError(message = "Field is required", target = fname))
        
        # TODO: run sql injection attack checks
        
        # if we get past the requiredness check, let run the specified validators
        elif finst.__contains__('checks') and finst['checks']:
            # iterate through the validators and dynamically run
            for check_name in finst['checks']:
                logging.info("running check %s for field %s\n" % (check_name, fname))
                
                # ask the validator to run the required check
                try:
                    # print >> sys.stderr, "attempting to call module function %s" % dir(validators),
                    validated_fieldvalues[fname] = vinst.check(check_name, field_value)
                except ValidateError, err:
                    logging.info(sys.stderr, "Caught validation error %s" % err)
                    errors.append(APIValidationError(message = err, target = fname))
    
                    
    return validated_fieldvalues

# TODO: move this to the module aswell
def render_errors(errors):
    # TODO: make this JSON serialization more robust
    return HttpResponse(simplejson.dumps([e.__json__() for e in errors]))


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
            'required': True
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
            'checks': ['integer'],
        }}

    # ask for some validation
    errors = [];
    apigen_validate(request, param_instructions, errors)
    
    # if we have validation errors then wrap a validaton error response
    if (errors):
        return render_errors(errors)
    else:
        return HttpResponse("ALL OK")