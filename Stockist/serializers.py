from rest_framework import serializers
from rest_framework.response import Response

from Company.serializers import CompanySerializers
from Stockist.models import *


class StockistSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stockist
        fields = '__all__'

class CompanyStockistSerializersWithOutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True,
                                  required=False)
    class Meta:
        model = CompanyStockist
        fields = '__all__'

class CompanyStockistSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True,
                                  required=False)
    stockist_name = StockistSerializers(allow_null=True,
                                        required=False)
    class Meta:
        model = CompanyStockist
        fields = '__all__'
    
    def create(self, validated_data):
        stockist_data = validated_data.get('stockist_name')
        stockist = Stockist(
            stockist_name = stockist_data['stockist_name'],
            stockist_address = stockist_data['stockist_address'],
            stockist_contact_number = stockist_data['stockist_contact_number'],
            stockist_territory=stockist_data['stockist_territory'],
            pan_vat_number = stockist_data['pan_vat_number'],
            stockist_category = stockist_data['stockist_category']
        )
        stockist.save()
        company_stockist = CompanyStockist(
            stockist_name = stockist,
            company_name = validated_data['company_name']
        )
        company_stockist.save()
        return company_stockist
    
    def update(self, instance, validated_data):
        stockist_instance = validated_data.get('stockist_name')
        stockist = Stockist.objects.get(id=instance.stockist_name.id)
        stockist.stockist_name = stockist_instance['stockist_name']
        stockist.stockist_address = stockist_instance[   
        'stockist_address']
        stockist.stockist_contact_number = stockist_instance[
        'stockist_contact_number']
        stockist.pan_vat_number = stockist_instance['pan_vat_number']
        stockist.stockist_territory = stockist_instance['stockist_territory']
        stockist.stockist_category = stockist_instance['stockist_category']
        stockist.save()
        instance.save()
        return instance


class StockistAddSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=200)
    class Meta:
        model = Stockist
        fields = ['stockist_address',
                  'stockist_category',
                  'stockist_name',
                  'stockist_contact_number',
                  'company_name',
                  ]
    
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data): 
        return Stockist.objects.create_stockist_with_signal(
                    stockist_name=validated_data.get('stockist_name'),
                    stockist_address=validated_data.get('stockist_address'),
                    stockist_category=validated_data.get('stockist_category'),
                    stockist_contact_number=validated_data.get(
                                                            'stockist_contact_number'
                                                            ),
                    company_name=validated_data.get('company_name')
                    )
    

class CompanyMPOStockistSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyMPOStockist
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['stockist_name'] = CompanyStockistSerializers(
            instance.stockist_name
        ).data
        return response