from django.conf.urls.defaults import *

urlpatterns = patterns('taskoverflow.api_views',
    (r'task/update/(?P<key>.+)*$', 'task_update'),
    (r'task/create', 'task_create'),
) + patterns('taskoverflow.api_search',
    r'task/search','task_search')