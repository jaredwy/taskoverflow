# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^foo/', include('foo.urls')),
    (r'^task/new/$', 'taskoverflow.views.task_new'),
    (r'^task/(?P<task_id>\d+)/$', 'taskoverflow.views.task_view'),
    # Tasks stuff
    (r'^tasks/search*', 'taskoverflow.views.tasks_search'),
    (r'^tasks/recent*', 'taskoverflow.views.tasks_recent'),
    (r'^tasktemplate/(?P<tasktemplate_id>\d+)/$', 'taskoverflow.views.tasktemplate'),
    # User stuff
    (r'^user/(?P<user_id>\d+)/$', 'taskoverflow.views.user_view'),
    (r'^test/create$', 'taskoverflow.views.create_data'),
    (r'^test/delete$', 'taskoverflow.views.delete_data'),
    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
    (r'^api/', include('taskoverflow.api_urls')),
    # reference the api urls
    
)
