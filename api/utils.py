from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.utils import timezone


from xhtml2pdf import pisa
from io import BytesIO
from . import models

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class InvoiceContext:
    def __init__(self, company, product, productAmount, userID):
        baseFEE = 500.0
        price = float(product.get('price'))
        productAmount = float(productAmount)

        liquidTAX = ((productAmount * price + baseFEE)  * product.get('tax'))
        totalPRODUCT = (product.get('price') * productAmount)
        product['formatedTax'] = f"{product.get('tax') * 100:.2f}%"
        product['liquidTax'] = f"$ {liquidTAX:.2f}"
        product['totalLiquid'] = f"$ {totalPRODUCT:.2f}"
        product['totalAfterTax'] = f"$ {(totalPRODUCT + liquidTAX + baseFEE):.2f}"

        self.product = product
        self.productAmount = productAmount
        self.costumer = company
        self.total = totalPRODUCT + liquidTAX + baseFEE
        self.issueDate = timezone.now()
        self.costumerCELLPHONE = f"{self.costumer.cellphone[0:3]}-{self.costumer.cellphone[3:6]}-{self.costumer.cellphone[6:]}"
        self.employee = self.getEmployeeUsername(userID)
        self.orderID = self.getLatestOrder()

    @classmethod
    def getLatestOrder(cls):
        try:
            return models.Order.objects.latest('id').id + 1
        except Exception:
            return 0

    @classmethod
    def getEmployeeUsername(cls, userID):
        try:
            print(userID)
            user = User.objects.get(id=userID)
            return user.username
        except Exception as err:
            print(err)
            raise Exception(f"Failed to get user: {str(err)}")