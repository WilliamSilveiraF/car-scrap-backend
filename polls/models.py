from django.db import models

class Company(models.Model):
    name = models.TextField()
    ein = models.TextField()
    businessStructure = models.JSONField(default=dict)
    address = models.JSONField(default=dict)
    cellphone = models.TextField()
    creationDate = models.DateTimeField('date published')
    active = models.BooleanField()

class Order(models.Model):
    product = models.JSONField(default=dict)
    productAmount = models.IntegerField()
    #costumer ForeignKey USER
    total = models.FloatField()
    issueDate = models.TextField()
    base64 = models.TextField()

