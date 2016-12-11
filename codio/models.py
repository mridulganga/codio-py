from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.
class code(models.Model):
    title  = models.CharField(max_length=200)
    developer = models.ForeignKey("auth.User")
    add_date = models.DateTimeField(default=timezone.now)
    language = models.CharField(max_length=20)
    usage = models.TextField()
    code_text = models.TextField()   #the code
    input_output = models.TextField(null=True,blank=True)   #combined
    level_choices = (
        (0,"Beginner"),
        (1,"Intermediate"),
        (2,"Advanced"),
    )
    level = models.IntegerField(choices=level_choices,null=False,default=0)
    tags = models.TextField(null=True,blank=True)   #comma separated tags

    def __str__(self):
        return self.title

class notification(models.Model):
    text = models.TextField()
    user = models.ForeignKey("auth.User")
    add_date = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
