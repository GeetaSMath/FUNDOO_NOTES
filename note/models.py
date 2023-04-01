# Id
# title
# body
# user_id
# created_at
# updated_at
# collaborator_id
# label_id
import json
from datetime import datetime, timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from user_fundoo.models import User
from django_celery_beat.models import CrontabSchedule, PeriodicTask

class Labels(models.Model):
    """
     Labels Model : name, user_id, created_at, modified_at
    """
    name = models.CharField(max_length=150, unique=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

class Note(models.Model):
    """
            Notes Model : title, description, user_id, created_at, modified_at, collaborator, label...
    """
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels)

    isArchive = models.BooleanField(default=False)
    isTrash = models.BooleanField(default=False)
    color = models.CharField(max_length=10, null=True, blank=True)
    reminder = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='notes_images/', null=True, blank=True)


