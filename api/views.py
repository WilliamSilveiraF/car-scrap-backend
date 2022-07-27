from django.contrib.auth.models import User
from django.utils import timezone

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
            'auth/token',
            'auth/token/refresh'
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

class NewUserView(views.APIView):
    def post(self, request):
        user = request.data.pop('user')
        company = request.data.pop('company')
        try:
            user = self.createUser(user)
            company = self.createCompany(company, user)

            return Response({'company': serializers.CompanySerializer(company).data}, status=200)
        except Exception as error:
            return Response({'error': str(error)}, status=400)
        

    @classmethod
    def createUser(cls, user):
        try:
            password = user.pop('password')
            user = User.objects.create(**user)
            user.set_password(password)
            user.save()
            return user
        except Exception as err:
            raise Exception(f"Failed to create user: {str(err)}")

    @classmethod
    def createCompany(cls, company, user):
        try:
            company['creationDate'] = timezone.now()
            
            newCompany = models.Company.objects.create(**company)
            newCompany.user = user
            newCompany.save()
            return newCompany

        except Exception as err:
            raise Exception(f"Failed to create company: {str(err)}")
