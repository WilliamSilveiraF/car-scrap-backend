from django.db import models

class Company(models.Model):
    name = models.TextField()
    ein = models.TextField()
    businessStructure = models.JSONField()
    address = models.JSONField()
    cellphone = models.TextField()
    creationDate = models.DateTimeField('date published')
    active = models.BooleanField()

