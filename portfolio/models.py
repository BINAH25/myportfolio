from django.db import models
from datetime import datetime
# Create your models here.


class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    project = models.CharField(max_length=1000)
    message = models.CharField(max_length=100000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.firstname
    
