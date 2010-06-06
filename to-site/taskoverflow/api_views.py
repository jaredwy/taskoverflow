"""
Contains the API views for the 
"""

import sys
import logging
import datetime
import jsonpickle
from validator import Validator, ValidateError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson
from dataLayer import DataLayer

def create_error(error_type, **args):
    params = {
        'errorType': error_type
    }
    
    # iterate through the args
    for k, v in args.iteritems():
        params[k] = v
        
    return params


def is_datetime(value):
    # regex the value
    # search_results = re.search("(\d{4}\-\d{2}\-\d{2})\s?(\d{2}\:\d{2}:\d{0,2})")
    
    # check the results
    date_value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

    return date_value
        

# TODO: move this into a library out of the views (maybe??)
def apigen_validate(request, instructions, errors):
    # define the validated field values
    validated_fieldvalues = {}
    
    # create the validator 
    vinst = Validator({ 'datetime': is_datetime })
    
    # iterate through the instructions and check to see if everything stacks up
    for fname, finst in instructions.iteritems():
        logging.info("checking validity of field: %s\n" % fname)
        
        # get the field value
        field_value = None
        if request.POST.__contains__(fname):
            field_value = request.POST[fname]
            
        # save the field data to the dict
        validated_fieldvalues[fname] = field_value

        # if the field is required and no data is supplied then add a validation error
        if finst['required'] and (not field_value):
            errors.append(create_error("validation", message = "Field is required", target = fname))
        
        # TODO: run sql injection attack checks
        
        # if we get past the requiredness check, let run the specified validators
        elif finst.__contains__('checks') and finst['checks']:
            # iterate through the validators and dynamically run
            for check_name in finst['checks']:
                logging.info("running check %s\n" % check_name)
                
                # ask the validator to run the required check
                try:
                    # print >> sys.stderr, "attempting to call module function %s" % dir(validators),
                    validated_fieldvalues[fname] = vinst.check(check_name, field_value)
                except ValidateError, err:
                    logging.info("Caught validation error %s" % err.message)
                    errors.append(create_error("validation", message = err.message, target = fname))

                    
    return validated_fieldvalues

# TODO: move this to the module aswell
def render_errors(errors):
    # TODO: make this JSON serialization more robust
    return HttpResponse(simplejson.dumps(errors))


"""
Task update methods

TODO: add login decorator
"""
def task_update(request, key):
    if (request.method == 'POST'):
        logging.info("Got posted values")
    

    for k, v in request.POST.iteritems():
        logging.info("%(key)s: %(value)s\n" % {'key': k, 'value': v})

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
            'checks': ['datetime'],
        },
        'task_est': {
            'required': True,
            'checks': ['integer']
        },
        'task_typeid': {
            'required': True,
            # ADD CUSTOM VALIDATION TO CHECK FOR TASK TYPE EXISTANCE
        },
        'task_points': {
            'required': False,
            'checks': ['integer'],
        }}
        
    logging.info("got post values: %s" % request.POST)

    # ask for some validation
    errors = [];
    field_values = apigen_validate(request, param_instructions, errors)
    
    # if we have validation errors then wrap a validaton error response
    if (errors):
        return render_errors(errors)
    else:
        dl = DataLayer()
        dl.CreateTask(
            title = field_values['task_name'],
            expiration = field_values['task_expiration'],
            estimatedTime = field_values['task_est'],
            taskType = field_values['task_typeid'],
            points = field_values['task_points'])
            
        return HttpResponse("ALL OK")