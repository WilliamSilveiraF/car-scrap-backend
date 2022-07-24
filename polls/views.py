from . import serializers, models, utils
from rest_framework.response import Response
from rest_framework import views
from django.utils import timezone
import base64
from io import BytesIO
import json

class InvoiceContext:
    def __init__(self, companyID, product, productAmount, employee):
        baseFEE = 500.0
        liquidTAX = ((productAmount * product.get('price') + baseFEE)  * product.get('tax'))
        totalPRODUCT = (product.get('price') * productAmount)
        product['formatedTax'] = f"{product.get('tax') * 100:.2f}%"
        product['liquidTax'] = f"$ {liquidTAX:.2f}"
        product['totalLiquid'] = f"$ {totalPRODUCT:.2f}"
        product['totalAfterTax'] = f"$ {(totalPRODUCT + liquidTAX + baseFEE):.2f}"

        self.product = product
        self.productAmount = productAmount
        self.costumer = self.getCompany(companyID)
        self.total = totalPRODUCT + liquidTAX + baseFEE
        self.issueDate = timezone.now()
        self.costumerCELLPHONE = f"{self.costumer.cellphone[0:3]}-{self.costumer.cellphone[3:6]}-{self.costumer.cellphone[6:]}"
        self.employee = employee
        self.orderID = models.Order.objects.latest('id').id + 1

    def getCompany(self, companyID):
        try: 
            company = models.Company.objects.get(id=companyID)
            return company
        except models.Company.DoesNotExist:
            return 'error'

class InvoiceView(views.APIView):
    def post(self, request):
        employee = request.data.get('employee', False)
        companyID = request.data.get('companyID', False)
        product = request.data.get('product', False)
        productAmount = request.data.get('productAmount', False)
        
        if not employee or not companyID or not product or not productAmount:
            return Response({'error': 'Review the request body'}, status=412)
        
        invoice = vars(InvoiceContext(**request.data))
        invoicePDF = utils.render_to_pdf('invoice.html', invoice)
        binaryInvoice = BytesIO(invoicePDF.content)
        base64Invoice = f"data:application/pdf;base64,{base64.b64encode(binaryInvoice.getvalue()).decode('utf-8')}"
        
        invoice.pop('costumerCELLPHONE')
        invoice.pop('employee')
        invoice.pop('orderID')
        try:
            newOrder = models.Order.objects.create(**invoice, base64=base64Invoice)
            return Response(serializers.OrderSerializer(newOrder).data, status=201)
        except Exception as error:
            print(error)
            return Response(error, status=412)

    def __str__(self):
        return self.id