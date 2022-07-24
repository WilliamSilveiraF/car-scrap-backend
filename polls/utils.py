from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from . import models
from django.utils import timezone

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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