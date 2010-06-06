#!/opt/local/bin/python

import urllib

# define the base url
BASE_URL = ""

params = urllib.urlencode({
                        "task_name": "New Task Name",
                        "task_description": "Updated Task Description",
                        "task_expiration": "06/14/2011",
                        "task_estimatedtime": 45,
                        "task_template": 4,
                        "task_location": "-27.56, 153.234",
                        })

resphandle = urllib.urlopen("http://localhost:8080/api/task/create", data = params)
                        
print resphandle.read()