from django.conf.urls.defaults import *

urlpatterns = patterns('taskoverflow.api_views',
    (r'task/update/(?P<key>.+)*$', 'task_update'),
)