from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

# These are the possible status for a form
STATUS = (
    ('PUBLISHED', "published"), 
    ('DRAFT', "draft"),
    ('ACTIVE', "active")
)

class Component(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=STATUS, default='PUBLISHED')

    class Meta:
        db_table = 'task-table'
