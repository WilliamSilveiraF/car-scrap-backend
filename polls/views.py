from . import serializers, models, utils
from rest_framework.response import Response
from rest_framework import views
import base64
from io import BytesIO

from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer

class GetRoutesView(views.APIView):
    def get(self, request):
        routes = [
            '/token',
            '/token/refresh'
        ]
        return Response(routes, status=200)

class InvoiceView(views.APIView):
    def post(self, request):
        employee = request.data.get('employee', False)
        companyID = request.data.get('companyID', False)
        product = request.data.get('product', False)
        productAmount = request.data.get('productAmount', False)
        
        if not employee or not companyID or not product or not productAmount:
            return Response({'error': 'Review the request body'}, status=412)
        
        invoice = vars(utils.InvoiceContext(**request.data))
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