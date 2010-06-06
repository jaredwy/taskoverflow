"""
Contains the API views for the 
"""

import sys
import logging
import datetime
import models
import demjson
from validator import Validator, ValidateError
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
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
    try:
        date_value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    except ValueError, err:
        raise ValidateError("Invalid date format")

    return date_value
        

# TODO: move this into a library out of the views (maybe??)
def apigen_validate(param_container, instructions, errors):
    # define the validated field values
    validated_fieldvalues = {}
    
    # create the validator 
    vinst = Validator({ 'datetime': is_datetime })
    
    # iterate through the instructions and check to see if everything stacks up
    for fname, finst in instructions.iteritems():
        logging.info("checking validity of field: %s\n" % fname)
        
        # get the field value
        field_value = None
        if param_container.__contains__(fname):
            field_value = param_container[fname]
            
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
    return HttpResponse(demjson.encode(errors))


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
        'task_description': {
            'required': True,
        },
        'task_expiration': {
            'required': True,
            'checks': ['datetime'],
        },
        'task_estimatedtime': {
            'required': True,
            'checks': ['integer']
        },
        'task_template': {
            'required': True,
            'checks': ['integer'],
            # ADD CUSTOM VALIDATION TO CHECK FOR TASK TYPE EXISTANCE
        },
        'task_points': {
            'required': False,
            'checks': ['integer'],
        }}
        
    logging.info("got post values: %s" % request.POST)

    # ask for some validation
    errors = [];
    field_values = apigen_validate(request.POST, param_instructions, errors)
    
    # if we have validation errors then wrap a validaton error response
    if (errors):
        return render_errors(errors)
    else:
        # create the new task
        dl = DataLayer()
        api_response = {
            'message': 'Sucessfully created task',
            'id': dl.CreateTask(
                    title = field_values['task_name'],
                    expiration = field_values['task_expiration'],
                    estimatedTime = field_values['task_estimatedtime'],
                    taskType = field_values['task_template'],
                    points = field_values['task_points'],
                    description = field_values['task_description'])
        }
            
        return HttpResponse(demjson.encode(api_response))
        
def task_get(request, id):
    # get the datalasy
    dl = DataLayer()
    task_instance = dl.GetTask(int(id))
    
    # attempt to add 
    # datetime.datetime.__dict__['json_response'] = 
    
    return HttpResponse(demjson.encode(task_instance.__dict__))
    
        
"""
ENDPOINT:
/api/tasktype/create

DESCRIPTION:
Used to create a new task type in the model

METHODS:
POST

POSTDATA:
tasktype_name - the name of the template
tasktype_value - the value of the template
tasktype_template - a reference to the template
"""
def tasktype_create(request):
    return HttpResponse("Create a task")
    