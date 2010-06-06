from django.conf.urls.defaults import *

urlpatterns = patterns('taskoverflow.api_publish_views',
    (r'tweet', 'tweet'),
    (r'authorise', 'authorise'),
)