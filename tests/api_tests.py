#!/opt/local/bin/python

import urllib

# define the base url
BASE_URL = ""

params = urllib.urlencode({
                        "task_name": "New Task Name",
                        "task_description": "Updated Task Description"
                        })

resphandle = urllib.urlopen("http://localhost:8080/api/task/create", data = params)
                        
print resphandle.read()