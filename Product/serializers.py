from wsgiref import validate
from rest_framework import serializers

from Company.serializers import *

from Product.models import *
from DCRUser.logic import get_user_from_access
from Company.models import CompanyWiseDivision



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class CompanyProductSerializerWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    class Meta:
        model = CompanyProduct
        fields = '__all__'

class CompanyProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    class Meta:
        model = CompanyProduct
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            response['company_name'] = CompanySerializers(
                                        instance.company_name).data
            response['product_name'] = ProductSerializer(
                                        instance.product_name).data
        except:
            response['company_name'] = CompanySerializers(
                                    instance['company_name']).data
            response['product_name'] = ProductSerializer(
                                    instance['product_name']).data
        return response


class CompanyDivisionProductSerializers(serializers.ModelSerializer):

    product_name = ProductSerializer()

    class Meta:
        model = CompanyDivisionProduct
        fields = '__all__'

    def create(self, validated_data):
        product_data = validated_data.get('product_name')
        product = Product(
        product_name=product_data['product_name'],
        product_molecular_name=product_data[
            'product_molecular_name'],
        product_price_per_strip_in_mrp=product_data[
            'product_price_per_strip_in_mrp'
        ],
        product_price_for_stockist=product_data[
            'product_price_for_stockist'
        ],
        product_description=product_data[
            'product_description'
        ],
        product_image=product_data[
            'product_image'
        ]
        )
        product.save()
        company_product = CompanyProduct(
            company_name=validated_data.get('company_name'),
            product_name=product
        )
        company_product.save()
        company_division_product=CompanyDivisionProduct(
            company_name=validated_data.get('company_name'),
            division_name=CompanyWiseDivision.objects.get(
                id=validated_data['division_name'].id
                ),
            product_name=product,
            product_type=validated_data.get('product_type'),
            bonus=validated_data.get('bonus')
        )
        company_division_product.save()
        return company_division_product
    
    def update(self, instance, validated_data):
        product_details = validated_data.get('product_name')
        product = instance.product_name
        product.product_name = product_details[
            'product_name'
        ]
        product.product_molecular_name = product_details[
            'product_molecular_name'
            ]
        product.product_price_per_strip_in_mrp = product_details[
            'product_price_per_strip_in_mrp'
            ]
        product.product_price_for_stockist = product_details[
            'product_price_for_stockist'
            ]
        product.product_description = product_details[
            'product_description'
            ]
        product.product_image = product_details[
            'product_image'
            ]
        product.save()
        instance.division_name = CompanyWiseDivision.objects.get(
                id=validated_data['division_name'].id
                )
        instance.product_type = validated_data['product_type']
        instance.bonus = validated_data['bonus']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['division_name'] = CompanyWiseDivisionSerializers(
            instance.division_name
        ).data
        return response

# class CompanyMpoWiseProductSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyMpoWiseProduct
#         fields = '__all__'

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['company_name'] = CompanySerializers(
#                                     instance.company_name).data
#         response['product_name'] = ProductSerializer(
#                                     instance.product_name).data
#         response['mpo_name'] = CompanyMpoSerializer(
#                                     instance.mpo_name).data
#         return response

# class ProductAddSerializers(serializers.ModelSerializer):
    # company_name = serializers.CharField(max_length=400)
    # division_name = serializers.CharField(max_length=400)
    # mpo_name = serializers.CharField(max_length=400)
    # class Meta:
        # model =Product
        # fields = ['product_name',
        #           'product_molecular_name',
        #           'product_price_per_strip_in_mrp',
        #           'product_price_for_stockiest',
        #           'company_name',
        #           'division_name',
        #           'mpo_name',
        #           ]
        # fields = '__all__'
        
    # def validate(self, attrs):
    #     return attrs

    # def validate(self, attrs):
    #     return super().validate(attrs)

    # def create(self, validated_data):
    #     return Product.objects.create_product_with_signal(
    #                 product_name=validated_data['product_name'],
    #                 product_molecular_name=validated_data['product_molecular_name'],
    #                 product_price_per_strip_in_mrp=validated_data['product_price_per_strip_in_mrp'],
    #                 product_price_for_stockiest=validated_data['product_price_for_stockiest'],
    #                 company_name=validated_data['company_name'],
    #                 division_name=validated_data['division_name'],
    #                 mpo_name=validated_data['mpo_name']
    #                 )
    # def create(self, validated_data):
    #     product=Product(
    #                 product_name=validated_data.get('product_name'),
    #                 product_molecular_name=validated_data.get('product_molecular_name'),
    #                 product_price_per_strip_in_mrp=validated_data.get('product_price_per_strip_in_mrp'),
    #                 product_price_for_stockist=validated_data.get('product_price_for_stockist')
    #                 )
    #     product.save()
    #     return product