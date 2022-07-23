from . import serializers, models, utils
from django.http import HttpResponse
from rest_framework import views
from django.utils import timezone
import base64
from io import BytesIO

class InvoiceContext:
    def __init__(self):
        self.product = self.getProduct()
        self.productAmount = 10
        self.costumer = self.getCompany()
        self.total = 1000.00
        self.issuingUser = self.getIssuingUser()
        self.issueDate = timezone.now()

    def getProduct(self):
        return {'name': 'Product A', 'price': 10.00, 'active': True}

    def getCompany(self):
        company = models.Company.objects.get(id=1).__dict__
        return company

    def getIssuingUser(self):
        company = models.Company.objects.get(id=2).__dict__
        return company

class InvoiceView(views.APIView):
    def get(self, request):
        print(request.data)
        
        context = InvoiceContext()
        print(vars(context))
        invoicePDF = utils.render_to_pdf('invoice.html', vars(context))
        binaryInvoice = BytesIO(invoicePDF.content)
        base64Invoice = f"data:application/pdf;base64,{base64.b64encode(binaryInvoice.getvalue()).decode('utf-8')}"

        return HttpResponse(base64Invoice)

    def __str__(self):
        return self.id