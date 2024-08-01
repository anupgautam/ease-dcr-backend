from rest_framework import serializers
from Chemist.models import (
    Chemist,
    ChemistCategory,
    ChemistCompanyArea,
    ChemistWorkingArea,
    CompanyChemistCategory,
    CompanyWiseChemist)
from Company.serializers import CompanySerializers


class AddChemistSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=200)
    mpo_name = serializers.CharField(max_length=10)
    is_investment = serializers.BooleanField()
    
    class Meta:
        model = Chemist
        fields = ['chemist_name',
                'chemist_address',
                'chemist_phone_number',
                'company_name',
                'chemist_territory',
                'chemist_contact_person',
                'chemist_pan_number',
                'mpo_name',
                'chemist_category',
                'is_investment']

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return Chemist.objects.create_chemist_with_signal(
            chemist_name=validated_data['chemist_name'],
            chemist_address=validated_data['chemist_address'],
            chemist_phone_number=validated_data['chemist_phone_number'],
            company_name=validated_data['company_name'],
            chemist_category=validated_data['chemist_category'],
            chemist_territory=validated_data['chemist_territory'],
            chemist_contact_person=validated_data['chemist_contact_person'],
            chemist_pan_number=validated_data['chemist_pan_number'],
            mpo_name=validated_data['mpo_name'],
            is_investment=validated_data['is_investment']
        )
    
    def update(self, instance, validated_data):
        instance.chemist_name = validated_data.get('chemist_name')
        instance.chemist_address = validated_data.get('chemist_address')
        instance.chemist_phone_number = validated_data.get('chemist_phone_number')
        instance.chemist_area = validated_data.get('chemist_area')
        instance.company_name = validated_data.get('company_name')
        instance.chemist_territory = validated_data.get('chemist_territory')
        instance.chemist_contact_person = validated_data.get('chemist_contact_person')
        instance.chemist_pan_number = validated_data.get('chemist_pan_number')
        instance.mpo_name = validated_data.get('mpo_name')
        instance.chemist_category = validated_data.get('chemist_category')
        instance.is_investment = validated_data.get('is_investment')
        instance.save()
        return instance


class ChemistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemist
        fields = '__all__'


class ChemistCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemistCategory
        fields = '__all__'


class CompanyWiseChemistSerializerWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    class Meta:
        model = CompanyWiseChemist
        fields = '__all__'

        
class CompanyWiseChemistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True,
                                  required=False)
    class Meta:
        model = CompanyWiseChemist
        fields = '__all__'
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company_name'] = CompanySerializers(
                                    instance.company_name).data
        response['chemist_name'] = ChemistSerializer(
                                    instance.chemist_name).data
        return response


class WorkingAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemistWorkingArea
        fields = [
            'id',
            'working_area_name',
            ]


class CompanyChemistCategorySerializer(serializers.ModelSerializer):
    category_name = ChemistCategorySerializer()
    class Meta:
        model = CompanyChemistCategory
        fields = '__all__'

    def create(self, validated_data):
        doctor_category_instance = ChemistCategory(
            category_name=validated_data['category_name']['category_name']
        )
        doctor_category_instance.save()
        instance = CompanyChemistCategory(
            category_name=doctor_category_instance,
            company_name=validated_data['company_name']
        )
        instance.save()
        return instance

    
class ChemistCompanyAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChemistCompanyArea
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['company_name'] = CompanySerializers(
                                    instance.company_name).data
        response['area_name'] = WorkingAreaSerializer(
                                    instance.area_name).data
        return response


class ChemistSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chemist
        fields = '__all__'
