from rest_framework import serializers
from django.http import JsonResponse
from django.db.models.query import QuerySet
from datetime import datetime, date
from nepali_date_converter import nepali_today
from Mpo.models import TourPlan
from dailycallrecord.models import *
from Stockist.models import CompanyStockist
from Doctors.serializers import *
from Product.serializers import *
from Company.serializers import *
from Chemist.serializers import *
from Chemist.models import *
from Stockist.models import *
from Product.serializers import ProductSerializer
from Stockist.serializers import *
from Chemist.serializers import CompanyWiseChemistSerializer, ChemistSerializer
from Mpo.serializers import ActiveWorkingDaysSerializer
from dailycallrecord.utils import nepali_month_from_english
from .graph import OptimizedGraph
from Product.serializers import CompanyProductSerializer
from utility.logic import (CreateLogicID,
                           UpdateLogicID,
                           DeleteLogicID,
                           CreateArrayInsideDictionaryWithQuerySet,
                           CreateArrayInsideDictionaryWithoutQuerySet)
from Mpo.serializers import ShiftSerializer,CompanyMPOAreaSerializers
from DCRUser.serializers import CompanyUserRoleSerializers,CompanyUserRoleSerializersWithoutToRepresentation


class RewardsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    class Meta:
        model = Rewards
        fields = '__all__'


class DcrForDoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    expenses_name = serializers.CharField(
        allow_null=True,
        required=False)
    expenses = serializers.DecimalField(
        allow_null=True,
        required=False,
        max_digits=10,
        decimal_places=9)
    expenses_reasoning = serializers.CharField(
        allow_null=True,
        required=False
    )

    class Meta:
        model = DcrForDoctor
        fields = '__all__'
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     try:
    #         response['visited_doctor'] = CompanyWiseDoctorSerializer(
    #                                     instance.visited_doctor).data
    #         response['visited_area'] = CompanyAreaSerializers(
    #                                     instance.visited_area).data
    #         response['date'] = ActiveWorkingDaysSerializer(
    #                                     instance.date).data
    #     except:
    #         response['visited_doctor'] = CompanyWiseDoctorSerializer(
    #                                     instance['visited_doctor']).data
    #         response['visited_area'] = CompanyAreaSerializers(
    #                                     instance['visited_area']).data
    #         response['date'] = ActiveWorkingDaysSerializer(
    #                                     instance['date']).data
    #     return response


class DcrForDoctorSerializerWithToRepresentation(serializers.ModelSerializer):
    class Meta:
        model = DcrForDoctor
        fields = '__all__'

    def to_representation(self, instance):
            response = super().to_representation(instance)
            response['visited_doctor'] = CompanyWiseDoctorSerializer(
                                        instance.visited_doctor).data
            response['visited_area'] = CompanyMPOAreaSerializers(
                                        instance.visited_area).data
            return response


class ShiftwiseDcrForDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftWiseDcrForDoctor
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shift'] = ShiftSerializer(instance.shift).data
        response['dcr']  = DcrForDoctorSerializerWithToRepresentation(instance.dcr).data
        return response


class DcrForDoctorCompanyProductMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForDoctorCompanyProductMap
        fields = '__all__'


class DcrForDoctorRewardsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForDoctorRewardsMap
        fields = '__all__'


class DcrForDoctorCompanyRolesMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForDoctorCompanyRolesMap
        fields = '__all__'




DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA = [
        {
    'model': CompanyProduct,
    'mapped_model': DcrForDoctorCompanyProductMap,
    'fk_original': 'dcr_id',
    'fk_map': 'company_product_id',
    'serializer': CompanyProductSerializerWithoutToRepresentation,
    'mapped_serializer':DcrForDoctorCompanyProductMapSerializer,
    'model_field_name': 'company_product'
    },
        {
    'model': Rewards,
    'mapped_model': DcrForDoctorRewardsMap,
    'fk_original': 'dcr_id',
    'fk_map': 'reward_id',
    'serializer': RewardsSerializer,
    'mapped_serializer':DcrForDoctorRewardsMapSerializer,
    'model_field_name': 'rewards'
    },
        {
    'model': CompanyUserRole,
    'mapped_model': DcrForDoctorCompanyRolesMap,
    'fk_original': 'dcr_id',
    'fk_map': 'roles_id',
    'serializer': CompanyUserRoleSerializersWithoutToRepresentation,
    'mapped_serializer':DcrForDoctorCompanyRolesMapSerializer,
    'model_field_name': 'company_roles'
    },
]


class DCRProductRewardsRolesSerializer(serializers.Serializer):
    id = serializers.IntegerField(allow_null=True,
        required=False)
    date = serializers.DateField(allow_null=True,
                                       required=False)
    visited_area = CompanyAreaSerializersWithoutToRepresentation(allow_null=True,
                                       required=False)
    visited_doctor = CompanyWiseDoctorWithoutToRepresentation(allow_null=True,
                                       required=False)
    expenses_name = serializers.CharField(
        allow_null=True,
        required=False,
        )
    # expenses = serializers.DecimalField(
    #     allow_null=True,
    #     required=False,
    #     max_digits=20,
    #     decimal_places=2)
    expenses = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    expenses_reasoning = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True
    )
    company_product = CompanyProductSerializerWithoutToRepresentation(
        allow_null=True,
        required=False,
        many=True
    )
    rewards = RewardsSerializer(
        allow_null=True,
        required=False,
        many=True
    )
    company_roles = CompanyUserRoleSerializersWithoutToRepresentation(
        allow_null=True,
        required=False,
        many=True
    )
    class Meta:
            update_methods = ['PUT', 'PATCH']
            
    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self.context.get('request') == "GET":
            if response['visited_doctor'] is None:
                response['visited_doctor'] = None
            else:
                response['visited_doctor'] = response['visited_doctor']['id']
            if response['visited_area'] is None:
                response['visited_area'] = None
            else:
                response['visited_area'] = response['visited_area']['id']
            # response['date'] = response['date']['id']
        elif self.context.get('request') == "PATCH":
            response['visited_doctor'] = instance['visited_doctor_id']
            response['visited_area'] = instance['visited_area_id']
            # response['date'] = instance['date_id']
        else:
            dcr_instance = DcrForDoctor.objects.get(id=instance['id'])
            response['visited_area'] = (dcr_instance.visited_area.id)
            response['visited_doctor'] = (dcr_instance.visited_doctor.id)
            # response['date'] = (dcr_instance.date.id)
        return response

    def validate(self, attrs):
        tour_plan = TourPlan.objects.filter(select_the_date_id=attrs['date'])
        if not tour_plan[0].is_admin_opened:
            if date(nepali_today.year, nepali_today.month, nepali_today.day-3) > attrs['date']:
                raise serializers.ValidationError({'3 days quota already passed'})
        return super().validate(attrs)
    
    def create(self, validated_data):
        original_model = DcrForDoctor
        create_array = CreateArrayInsideDictionaryWithQuerySet
        CreateLogicID(
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            create_array).create()
        original_data = CreateLogicID(
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            create_array).create_return()
        return original_data

    def update(self, instance, validated_data):
        if validated_data['date']:
            date = validated_data['date']
            instance.month = nepali_month_from_english(date.strftime("%B"))
            instance.year = date.year
            instance.save()
        original_model = DcrForDoctor
        create_array = CreateArrayInsideDictionaryWithQuerySet
        if validated_data['visited_doctor'] is None:
            validated_data['visited_doctor'] = None
        else:
            validated_data['visited_doctor'] = validated_data['visited_doctor']['id']
        # if validated_data['date'] is None:
        #     validated_data['date'] = None
        # else:
        #     validated_data['date'] = validated_data['date']['id']
        if validated_data['visited_area'] is None:
            validated_data['visited_area'] = None
        else:
            validated_data['visited_area'] = validated_data['visited_area']['id']
        UpdateLogicID(
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update()
        original_data = UpdateLogicID(
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update_return()
        return original_data

    def delete(self, request, *args, **kwargs):
        original_model = DcrForDoctor
        create_array = CreateArrayInsideDictionaryWithQuerySet
        DeleteLogicID(
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            request,
            create_array,
            self.context
        ).delete()
        original_data = DeleteLogicID(
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            request,
            create_array,
            self.context
        ).delete_return()
        return original_data


class MpoWiseShiftWiseDcrForDoctorSerializer(
    serializers.ModelSerializer):
    dcr = ShiftwiseDcrForDoctorSerializer()

    class Meta:
        model = MpoWiseShiftwiseDcrForDoctor
        fields = '__all__'

    def create(self, validated_data):
        dcr_data = (validated_data['dcr'])
        shift_wise_dcr_instace = ShiftWiseDcrForDoctor(
            dcr=dcr_data['dcr'],
            shift=dcr_data['shift']
        )
        shift_wise_dcr_instace.save()
        mpo_wise_dcr_for_doctor_instance = MpoWiseShiftwiseDcrForDoctor(
            mpo_name=validated_data.get('mpo_name'),
            dcr = shift_wise_dcr_instace
        )
        mpo_wise_dcr_for_doctor_instance.save()
        return mpo_wise_dcr_for_doctor_instance
    
    def update(self, instance, validated_data):
        shift_wise_dcr_instance = ShiftWiseDcrForDoctor.objects.get(
            id=instance.dcr.id
        )
        shift_wise_dcr_instance.shift = validated_data['dcr']['shift']
        shift_wise_dcr_instance.save()
        instance.dcr = shift_wise_dcr_instance
        instance.mpo_name = validated_data['mpo_name']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mpo_name']  = CompanyUserRoleSerializers(
            instance.mpo_name).data
        return response

    
class ChemistOrderedProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False,
                                  allow_null=True)
    class Meta:
        model = ChemistOrderedProduct
        fields = '__all__'


class ChemistOrderedProductInformationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False,
                                  allow_null=True)
    class Meta:
        model = ChemistOrderedProductInformation
        fields = "__all__"


class ChemistOrderedProductInformationMapSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False,
                                  allow_null=True)
    class Meta:
        model = ChemistOrderedProductInformationMap
        fields = '__all__'


class DcrForChemistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False,
                                  allow_null=True)
    class Meta:
        model = DcrForChemist
        fields = '__all__'


class DcrForChemistProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForChemistProduct
        fields = '__all__'


class DcrForChemistPromotedProductMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForChemistPromotedProductMap
        fields = '__all__'


class DcrForChemistRewardsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForChemistRewardsMap
        fields = '__all__'


class DcrForChemistCompanyRolesMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForChemistCompanyRolesMap
        fields = '__all__'


DCR_ORDERED_PRODUCT_INFORMATION = [
    {
    'model': ChemistOrderedProductInformation,
    'mapped_model': ChemistOrderedProductInformationMap,
    'fk_original': 'product_id',
    'fk_map': 'information_id',
    'serializer': ChemistOrderedProductInformationSerializer,
    'mapped_serializer':ChemistOrderedProductInformationMapSerializer,
    'model_field_name': 'product_information'
    },
]


class DCRChemistOrderedProductInformationSerializer(serializers.Serializer):
    id= serializers.IntegerField(allow_null=True,
        required=False)
    # ordered_product = CompanyProductSerializer(
    #     allow_null=True,
    #     required=False,
    # )
    product_information = ChemistOrderedProductInformationSerializer(
        allow_null=True,
        required=False,
        many=True
    )
    class Meta:
            update_methods = ['PUT', 'PATCH']

    # def to_internal_value(self, data):
    #     response = data.copy()
    #     if isinstance(response.get('visited_chemist'), dict):
    #         response['visited_chemist'] = response['visited_chemist']
    #     else:
    #         response['visited_chemist'] = CompanyWiseChemist.objects.get(id=data.get('visited_chemist')).__dict__
    #     if isinstance(response['visited_area'], dict):
    #         response['visited_area'] = response['visited_area']
    #     else:
    #         response['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
    #     if isinstance(response['date'], dict):
    #         response['date'] = response['date']
    #     else:
    #         response['date'] = ActiveWorkingDays.objects.get(id=data.get('date')).__dict__
    #     return super().to_internal_value(response)

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     if self.context.get('request') == "GET":
    #         response['ordered_product'] = response['ordered_product']['id']
    #     elif self.context.get('request') == "PATCH":
    #         response['ordered_product'] = instance['ordered_product_id']
    #     else:
    #         dcr_instance = ChemistOrderedProduct.objects.get(id=instance['id'])
    #         response['ordered_product'] = (dcr_instance.ordered_product.id)
    #     return response
    # def validate(self, attrs):
        
        
        # return super().validate(attrs)
    
    
    def create(self, validated_data):
        original_model = DcrForChemistProduct
        create_array = CreateArrayInsideDictionaryWithQuerySet
        CreateLogicID(
            DCR_ORDERED_PRODUCT_INFORMATION,
            original_model,
            validated_data,
            create_array).create()
        original_data = CreateLogicID(
            DCR_ORDERED_PRODUCT_INFORMATION,
            original_model,
            validated_data,
            create_array).create_return()
        return original_data

    def update(self, instance, validated_data):
        original_model = DcrForChemistProduct
        create_array = CreateArrayInsideDictionaryWithQuerySet
        # if validated_data['ordered_product'] is None:
        #     validated_data['ordered_product'] = None
        # else:
        #     validated_data['ordered_product'] = validated_data['ordered_product']['id']
        UpdateLogicID(
            DCR_ORDERED_PRODUCT_INFORMATION,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update()
        original_data = UpdateLogicID(
            DCR_ORDERED_PRODUCT_INFORMATION,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update_return()
        return original_data

    def delete(self, request, *args, **kwargs):
        original_model = DcrForChemistProduct
        create_array = CreateArrayInsideDictionaryWithQuerySet
        DeleteLogicID(
            DCR_ORDERED_PRODUCT_INFORMATION,
            original_model,
            request,
            create_array,
            self.context
        ).delete()
        original_data = DeleteLogicID(
            DCR_ORDERED_PRODUCT_INFORMATION,
            original_model,
            request,
            create_array,
            self.context
        ).delete_return()
        
        return original_data


DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA = [
        {
    'model': CompanyProduct,
    'mapped_model': DcrForChemistPromotedProductMap,
    'fk_original': 'dcr_id',
    'fk_map': 'company_product_id',
    'serializer': CompanyProductSerializerWithoutToRepresentation,
    'mapped_serializer':DcrForChemistPromotedProductMapSerializer,
    'model_field_name': 'company_product'
    },
        {
    'model': Rewards,
    'mapped_model': DcrForChemistRewardsMap,
    'fk_original': 'dcr_id',
    'fk_map': 'reward_id',
    'serializer': RewardsSerializer,
    'mapped_serializer':DcrForChemistRewardsMapSerializer,
    'model_field_name': 'rewards'
    },
        {
    'model': CompanyUserRole,
    'mapped_model': DcrForChemistCompanyRolesMap,
    'fk_original': 'dcr_id',
    'fk_map': 'roles_id',
    'serializer': CompanyUserRoleSerializersWithoutToRepresentation,
    'mapped_serializer':DcrForChemistCompanyRolesMapSerializer,
    'model_field_name': 'company_roles'
    },
        {
    'model': CompanyProduct,
    'mapped_model': DcrForChemistProduct,
    'fk_original': 'dcr_id',
    'fk_map': 'ordered_product',
    'serializer': CompanyProductSerializerWithoutToRepresentation,
    'mapped_serializer':DcrForChemistProductSerializer,
    'model_field_name': 'ordered_products'
    }
]


class DCRChemistProductRewardsRolesSerializer(serializers.Serializer):
    id= serializers.IntegerField(allow_null=True,
        required=False)
    date = serializers.DateField(allow_null=True,
                                       required=False,
                                       )
    visited_area = CompanyAreaSerializersWithoutToRepresentation(allow_null=True,
                                       required=False)
    visited_chemist = CompanyWiseChemistSerializerWithoutToRepresentation(allow_null=True,
                                       required=False)
    expenses_name = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True)
    # expenses = serializers.DecimalField(
    #     allow_null=True,
    #     required=False,
    #     max_digits=20,
    #     decimal_places=2)
    expenses = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    expenses_reasoning = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True
    )
    company_product = CompanyProductSerializerWithoutToRepresentation(
        allow_null=True,
        required=False,
        many=True
    )
    rewards = RewardsSerializer(
        allow_null=True,
        required=False,
        many=True
    )
    company_roles = CompanyUserRoleSerializersWithoutToRepresentation(
        allow_null=True,
        required=False,
        many=True
    )
    ordered_products = CompanyProductSerializerWithoutToRepresentation(
        allow_null=True,
        required=False,
        many=True
    )
    class Meta:
            update_methods = ['PUT', 'PATCH']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self.context.get('request') == "GET":
            if response['visited_chemist'] is None:
                response['visited_chemist'] = None
            else:
                response['visited_chemist'] = response['visited_chemist']['id']
            if response['visited_area'] is None:
                response['visited_area'] = None
            else:
                response['visited_area'] = response['visited_area']['id']
        elif self.context.get('request') == "PATCH":
            response['visited_chemist'] = instance['visited_chemist_id']
            response['visited_area'] = instance['visited_area_id']
        else:
            dcr_instance = DcrForChemist.objects.get(id=instance['id'])
            if response['visited_area'] is None:
                response['visited_area'] = None
            else:
                response['visited_area'] = (dcr_instance.visited_area.id)
            if response['visited_chemist'] is None:
                response['visited_area'] = None
            else:
                response['visited_chemist'] = (dcr_instance.visited_chemist.id)
        return response

    def validate(self, attrs):
        return super().validate(attrs)
    
    def create(self, validated_data):
        original_model = DcrForChemist
        create_array = CreateArrayInsideDictionaryWithQuerySet
        CreateLogicID(
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            create_array).create()
        original_data = CreateLogicID(
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            create_array).create_return()
        return original_data

    def update(self, instance, validated_data):
        if validated_data['date']:
            date = validated_data['date']
            instance.month = nepali_month_from_english(date.strftime("%B"))
            instance.year = date.year
            instance.save()
        original_model = DcrForChemist
        create_array = CreateArrayInsideDictionaryWithQuerySet
        if validated_data['visited_chemist'] is None:
            validated_data['visited_chemist'] = None
        else:
            validated_data['visited_chemist'] = validated_data['visited_chemist']['id']
        if validated_data['visited_area'] is None:
            validated_data['visited_area'] = None
        else:
            validated_data['visited_area'] = validated_data['visited_area']['id']
        UpdateLogicID(
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update()
        original_data = UpdateLogicID(
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update_return()
        return original_data

    def delete(self, request, *args, **kwargs):
        original_model = DcrForChemist
        create_array = CreateArrayInsideDictionaryWithQuerySet
        DeleteLogicID(
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            request,
            create_array,
            self.context
        ).delete()
        original_data = DeleteLogicID(
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            request,
            create_array,
            self.context
        ).delete_return() 
        return original_data


class DcrForChemistSerializerWithToRepresentation(serializers.ModelSerializer):
    class Meta:
        model = DcrForChemist
        fields = '__all__'
    def to_representation(self, instance):
            response = super().to_representation(instance)
            response['visited_chemist'] = CompanyWiseChemistSerializer(
                                        instance.visited_chemist).data
            response['visited_area'] = CompanyMPOAreaSerializers(
                                        instance.visited_area).data
            return response


class ShiftwiseDcrForChemistSerializer(serializers.ModelSerializer):
    # dcr = DcrForChemistSerializer()
    class Meta:
        model = ShiftWiseDcrForChemist
        fields = '__all__'
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shift'] = ShiftSerializer(instance.shift).data
        response['dcr']  = DcrForChemistSerializerWithToRepresentation(instance.dcr).data
        return response

class MpoWiseShiftWiseDcrForChemistSerializer(
    serializers.ModelSerializer):
    dcr = ShiftwiseDcrForChemistSerializer()

    class Meta:
        model = MpoWiseShiftwiseDcrForChemist
        fields = '__all__'
    
    def create(self, validated_data):
        # dcr_with_shift_data = (validated_data.get('dcr'))
        dcr_data = validated_data['dcr']
        # dcr_instance = DcrForChemist(
        #     **dcr_data
        # )
        # dcr_instance.save()
        shift_wise_dcr_instace = ShiftWiseDcrForChemist(
            dcr=dcr_data['dcr'],
            shift=dcr_data['shift']
        )
        shift_wise_dcr_instace.save()
        mpo_wise_dcr_for_chemist_instance = MpoWiseShiftwiseDcrForChemist(
            mpo_name=validated_data.get('mpo_name'),
            dcr = shift_wise_dcr_instace
        )
        mpo_wise_dcr_for_chemist_instance.save()
        return mpo_wise_dcr_for_chemist_instance
    
    def update(self, instance, validated_data):
        shift_wise_dcr_instance = ShiftWiseDcrForChemist.objects.get(
            id=instance.dcr.id
        )
        shift_wise_dcr_instance.shift = validated_data['dcr']['shift']
        shift_wise_dcr_instance.save()
        instance.dcr = shift_wise_dcr_instance
        instance.mpo_name = validated_data['mpo_name']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mpo_name']  = CompanyUserRoleSerializers(
            instance.mpo_name).data
        return response


class StockistOrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockistOrderedProduct
        fields = '__all__'
        read_only_fields = ('order_value',)


class StockistOrderedProductSerializerWithToRepresentation(serializers.ModelSerializer):
    class Meta:
        model = StockistOrderedProduct
        fields = '__all__'
        read_only_fields = ('order_value',)
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['ordered_product'] = CompanyProductSerializer(
            instance.ordered_product
        ).data
        return response


class DcrForStockistSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        required=False,
        allow_null=True
    )
    class Meta:
        model = DcrForStockist
        fields = '__all__'


class DcrForStockistSerializerWithToRepresentation(serializers.ModelSerializer):
    class Meta:
        model = DcrForStockist
        fields = '__all__'
    def to_representation(self, instance):
            response = super().to_representation(instance)
            response['visited_stockist'] = CompanyStockistSerializers(
                                        instance.visited_stockist).data
            response['visited_area'] = CompanyAreaSerializers(
                                        instance.visited_area).data
            return response


class DcrForStockistOrderedProductSerializer(serializers.ModelSerializer):
    ordered_product = StockistOrderedProductSerializer()

    class Meta:
        model = DcrForStockistOrderedProduct
        fields = '__all__'

    def create(self, validated_data):
        order_product_instance = StockistOrderedProduct(
            **validated_data['ordered_product']
        )
        order_product_instance.save()
        dcr_stockist_ordered_product = DcrForStockistOrderedProduct(
            dcr_id=validated_data['dcr_id'],
            ordered_product = order_product_instance
        )
        dcr_stockist_ordered_product.save()
        return dcr_stockist_ordered_product
    
    def update(self, instance, validated_data):
        ordered_product_instance = StockistOrderedProduct.objects.get(id=instance.ordered_product.id)
        ordered_product_instance.ordered_product = validated_data['ordered_product']['ordered_product']
        ordered_product_instance.ordered_quantity = validated_data['ordered_product']['ordered_quantity']
        ordered_product_instance.save()
        instance.ordered_product = ordered_product_instance
        instance.save()
        return instance
        # return super().update(instance, validated_data)

 
# class DcrForStockistOrderedProductMapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DcrForStockistOrderedProductMap
#         fields = '__all__'


class DcrForStockistRewardsMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForStockistRewardsMap
        fields = '__all__'


class DcrForStockistCompanyRolesMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = DcrForStockistCompanyRolesMap
        fields = '__all__'


DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA = [
        {
    'model': Rewards,
    'mapped_model': DcrForStockistRewardsMap,
    'fk_original': 'dcr_id',
    'fk_map': 'reward_id',
    'serializer': RewardsSerializer,
    'mapped_serializer':DcrForStockistRewardsMapSerializer,
    'model_field_name': 'rewards'
    },
        {
    'model': CompanyUserRole,
    'mapped_model': DcrForStockistCompanyRolesMap,
    'fk_original': 'dcr_id',
    'fk_map': 'roles_id',
    'serializer': CompanyRolesSerializersWithoutToRepresentation,
    'mapped_serializer':DcrForStockistCompanyRolesMapSerializer,
    'model_field_name': 'company_roles'
    },
    #     {
    # 'model': StockistOrderedProduct,
    # 'mapped_model': DcrForStockistOrderedProduct,
    # 'fk_original': 'dcr_id',
    # 'fk_map': 'ordered_product',
    # 'serializer': StockistOrderedProductSerializer,
    # 'mapped_serializer':DcrForStockistOrderedProductSerializer,
    # 'model_field_name': 'ordered_products'
    # }
]

class DCRStockistProductRewardsRolesSerializer(serializers.Serializer):
    id= serializers.IntegerField(allow_null=True,
        required=False)
    date = serializers.DateField(allow_null=True,
                                       required=False)
    visited_area = CompanyAreaSerializersWithoutToRepresentation(allow_null=True,
                                       required=False)
    visited_stockist = CompanyStockistSerializersWithOutToRepresentation(
        allow_null=True,
        required=False
    )
    expenses_name = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True)
    # expenses = serializers.DecimalField(
    #     allow_null=True,
    #     required=False,
    #     max_digits=10,
    #     decimal_places=9)
    expenses = serializers.IntegerField(
        allow_null=True,
        required=False
    )
    expenses_reasoning = serializers.CharField(
        allow_null=True,
        required=False,
        allow_blank=True
    )
    rewards = RewardsSerializer(
        allow_null=True,
        required=False,
        many=True
    )
    company_roles = CompanyUserRoleSerializersWithoutToRepresentation(
        allow_null=True,
        required=False,
        many=True
    )
    # ordered_products = StockistOrderedProductSerializer(
    #     allow_null=True,
    #     required=False,
    #     many=True
    # )
    class Meta:
            update_methods = ['PUT', 'PATCH']

    # def to_internal_value(self, data):      
    #     response = data.copy()
    #     if isinstance(response.get('visited_stockist'), dict):
    #         response['visited_stockist'] = response['visited_chemist']
    #     else:
    #         response['visited_stockist'] = CompanyStockist.objects.get(id=data.get('visited_stockist')).__dict__
    #     if isinstance(response['visited_area'], dict):
    #         response['visited_area'] = response['visited_area']
    #     else:
    #         response['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
    #     if isinstance(response['date'], dict):
    #         response['date'] = response['date']
    #     else:
    #         response['date'] = ActiveWorkingDays.objects.get(id=data.get('date')).__dict__
    #     return super().to_internal_value(response)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if self.context.get('request') == "GET":
            if response['visited_stockist'] is None:
                response['visited_stockist'] = None
            else:
                response['visited_stockist'] = response['visited_stockist']['id']
            if response['visited_area'] is None:
                response['visited_area'] = None
            else:
                response['visited_area'] = response['visited_area']['id']
        elif self.context.get('request') == "PATCH":
            response['visited_stockist'] = instance['visited_stockist_id']
            response['visited_area'] = instance['visited_area_id']
        else:
            dcr_instance = DcrForStockist.objects.get(id=instance['id'])
            if response['visited_area'] is None:
                response['visited_area'] = None
            else:
                response['visited_area'] = (dcr_instance.visited_area.id)
            if response['visited_stockist'] is None:
                response['visited_area'] = None
            else:
                response['visited_stockist'] = (dcr_instance.visited_stockist.id)
        return response
    
    def validate(self, attrs):  
        return super().validate(attrs)
    
    def create(self, validated_data):
        for order_dict in validated_data['ordered_products']:
            order_dict['order_value'] = (CompanyProduct.objects.get(id=order_dict['ordered_product'].id)).product_name.product_price_for_stockist * int(order_dict['ordered_quantity']) 
        original_model = DcrForStockist
        create_array = CreateArrayInsideDictionaryWithQuerySet
        CreateLogicID(
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            create_array).create()
        original_data = CreateLogicID(
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            create_array).create_return()
        return original_data

    def update(self, instance, validated_data):
        if validated_data['date']:
            date = validated_data['date']
            instance.month = nepali_month_from_english(date.strftime("%B"))
            instance.year = date.year
            instance.save()
        original_model = DcrForStockist
        create_array = CreateArrayInsideDictionaryWithQuerySet
        if validated_data['visited_stockist'] is None:
                validated_data['visited_stockist'] = None
        else:
            validated_data['visited_stockist'] = validated_data['visited_stockist']['id']
        if validated_data['visited_area'] is None:
            validated_data['visited_area'] = None
        else:
            validated_data['visited_area'] = validated_data['visited_area']['id']
            # for order_dict in validated_data['ordered_products']:
            #     if validated_data['ordered_products'] and order_dict['ordered_quantity']:
            #         order_dict['order_value'] = (CompanyProduct.objects.get(id=order_dict['id'])).product_name.product_price_for_stockist * int(order_dict['ordered_quantity'])    
        UpdateLogicID(
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update()
        original_data = UpdateLogicID(
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            validated_data,
            instance,
            self.context,
            create_array
        ).update_return()
        return original_data

    def delete(self, request, *args, **kwargs):
        original_model = DcrForStockist
        create_array = CreateArrayInsideDictionaryWithQuerySet
        DeleteLogicID(
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            request,
            create_array,
            self.context
        ).delete()
        original_data = DeleteLogicID(
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA,
            original_model,
            request,
            create_array,
            self.context
        ).delete_return()
        return original_data


class ShiftwiseDcrForStockistSerializer(serializers.ModelSerializer):
    # dcr = DcrForStockistSerializer()
    class Meta:
        model = ShiftWiseDcrForStockist
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shift'] = ShiftSerializer(instance.shift).data
        response['dcr']  = DcrForStockistSerializerWithToRepresentation(instance.dcr).data
        return response


class MpoWiseShiftWiseDcrForStockistSerializer(
    serializers.ModelSerializer):
    dcr = ShiftwiseDcrForStockistSerializer()

    class Meta:
        model = MpoWiseShiftwiseDcrForStockist
        fields = '__all__'

    def create(self, validated_data):
        dcr_data = validated_data['dcr']
        shift_wise_dcr_instace = ShiftWiseDcrForStockist(
            dcr=dcr_data['dcr'],
            shift=dcr_data['shift']
        )
        shift_wise_dcr_instace.save()
        mpo_wise_dcr_for_chemist_instance = MpoWiseShiftwiseDcrForStockist(
            mpo_name=validated_data.get('mpo_name'),
            dcr = shift_wise_dcr_instace
        )
        mpo_wise_dcr_for_chemist_instance.save()
        return mpo_wise_dcr_for_chemist_instance
    
    def update(self, instance, validated_data):
        shift_wise_dcr_instance = ShiftWiseDcrForStockist.objects.get(
            id=instance.dcr.id
        )
        shift_wise_dcr_instance.shift = validated_data['dcr']['shift']
        shift_wise_dcr_instance.save()
        instance.dcr = shift_wise_dcr_instance
        instance.mpo_name = validated_data['mpo_name']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mpo_name']  = CompanyUserRoleSerializers(
            instance.mpo_name).data
        return response
