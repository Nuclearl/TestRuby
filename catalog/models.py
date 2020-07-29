from django.db import models


# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=1000, help_text="Enter a  project")

    def __str__(self): return self.name


class Record(models.Model):
    text = models.CharField(max_length=1000, help_text="Enter a task")
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=False)
    def __str__(self): return self.text

