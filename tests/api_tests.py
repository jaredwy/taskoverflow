#!/opt/local/bin/python

import urllib

# define the base url
BASE_URL = ""

params = urllib.urlencode({
                        "task_name": "New Task Name",
                        "task_description": "Updated Task Description",
                        "task_expiration": "2009-07-01 13:00:43",
                        "task_est": 45,
                        "task_typeid": 4
                        })

resphandle = urllib.urlopen("http://localhost:8080/api/task/create", data = params)
                        
print resphandle.read()