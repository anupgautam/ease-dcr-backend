from rest_framework import serializers
from Payment.models import *


class BankSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class CompanyWiseBankSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyWiseBank
        fields = '__all__'


class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class StockistPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockistPayment
        fields = '__all__'