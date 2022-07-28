from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    STRUCTURE = (
        ('LLC', 'LIMITED LIABILITY COMPANY'),
        ('SP', 'SOLE PROPRIETORSHIPS'),
        ('PARTNER', 'PARTNERSHIP'),
        ('CORP', 'CORPORATION'),
        ('S CORP', 'S CORPORATION'),
        ('ND', 'NOT DEFINED')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.TextField()
    ein = models.TextField()
    structure = models.CharField(max_length=7,choices=STRUCTURE, default='ND')
    address = models.JSONField(default=dict)
    cellphone = models.TextField()
    creationDate = models.DateTimeField()
    active = models.BooleanField(default=True)

class Order(models.Model):
    product = models.JSONField(default=dict)
    productAmount = models.IntegerField()
    costumer = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    total = models.FloatField()
    issueDate = models.TextField()
    base64 = models.TextField(null=True)