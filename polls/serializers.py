from django.utils import timezone
from . import models
from rest_framework import serializers

class CompanySerializer(serializers.Serializer):
    class Meta:
        model = models.Company
        fields = '__all__'

    def create(data):
        try:
            newCompany = models.Company.objects.create(
                name=data.get('name'),
                ein=data.get('ein'),
                businessStructure=data.get('businessType'),
                address=data.get('address'),
                creationDate=timezone.now(),
                cellphone=data.get('cellphone'),
                active=True
            )

            return newCompany

        except Exception as error:
            print(error)
            return error