from google.appengine.ext.db import djangoforms
import models

class TaskForm(djangoforms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ['taskType','taskState']
