"""
Contains the API views for the publishing modules (for export to Twitter and other export destinations)
"""

import sys
import logging
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson

import publishing
from twitteroauth import TwitterNotAuthorisedError


CONSUMER_KEY = 'FUja3lLCyC4zWe5PmGdfQ'
CONSUMER_SECRET = '4vjeFWOYWF3eGqHzoVvhzJSZdkhaHTcbJsfFz3qUBnY'

"""
ENDPOINT:
/publish/tweet

DESCRIPTION:
Used to post an aggregated update message of tasks to a pre-configured Twitter account

METHODS: 
POST

POSTDATA:
None
"""
def tweet(request):
    
    # ask for some validation
    errors = [];
    publisher = publishing.PublisherApi('twitter', request, None, CONSUMER_KEY, CONSUMER_SECRET)
    result = 'Failed'
    try:
        result = publisher.publish()
    except TwitterNotAuthorisedError:
        return authorise(request)
        
    return HttpResponse("Result: %s" % result)
    
def authorise(request):
    
    # redirect the user to authorise this to for Twitter Access
    publisher = publishing.PublisherApi('twitter', request, None, CONSUMER_KEY, CONSUMER_SECRET)
    publisher.callback();
    return publisher.response