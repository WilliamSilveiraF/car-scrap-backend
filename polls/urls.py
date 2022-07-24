from django.urls import path
from . import views

urlpatterns = [
    path('', views.InvoiceView.as_view(), name='Invoice')
]