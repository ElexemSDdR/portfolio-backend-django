# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from uuid import uuid4

class Project(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    title = models.CharField(null=False)
    description = models.TextField(null=False)
    technologies = models.JSONField()
    url = models.CharField(null=False)
    githubrepo = models.CharField(db_column='githubRepo', null=False, blank=True, default='')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'project'
