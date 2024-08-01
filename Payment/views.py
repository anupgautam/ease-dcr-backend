from rest_framework import viewsets
from Payment.serializers import *


class BankViewset(viewsets.ModelViewSet):
    model = Bank
    queryset = Bank.objects.all()
    serializer_class = BankSerializers


class CompanyWiseBankViewset(viewsets.ModelViewSet):
    model = CompanyWiseBank
    queryset = CompanyWiseBank.objects.all()
    serializer_class = CompanyWiseBankSerializers


class PaymentViewset(viewsets.ModelViewSet):
    model = Payment
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializers


class StockistPaymentViewset(viewsets.ModelViewSet):
    model = StockistPayment
    queryset = StockistPayment.objects.all()
    serializer_class = StockistPaymentSerializer