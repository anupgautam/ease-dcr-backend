from http.client import BAD_REQUEST
from django.http import HttpResponseBadRequest
from rest_framework import serializers
from rest_framework.decorators import action
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone


from DCRUser.serializers import UserSerializers
from Mpo.models import *
from Company.serializers import CompanySerializers
from Company.serializers import CompanyRolesSerializers
from Mpo.utils import mpo_data_transmission
from Doctors.serializers import DoctorSerializers
from DCRUser.models import CompanyUserRole
from DCRUser.serializers import CompanyUserRoleSerializers
from Chemist.serializers import CompanyWiseChemistSerializer
from Stockist.serializers import CompanyStockistSerializers
from Company.serializers import CompanyAreaSerializers


# class CompanyMpoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyMpo
#         fields = '__all__'
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['company_name'] = CompanySerializers(
#                                     instance.company_name).data
#         response['mpo_name'] = UserSerializers(
#                                     instance.mpo_name).data
#         return response


class ShiftSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    class Meta:
        model = Shift
        fields = '__all__'


class CompanyDivisionWiseMpoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDivisionWiseMpo
        fields = '__all__'


# class AreaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Area
#         fields = '__all__'


# class CompanyWiseAreaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyWiseArea
#         fields = '__all__'


class PurposeOfVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurposeOfVisit
        fields = '__all__'


#for bulk create
class ActiveWorkingDaysListSerializer(serializers.ListSerializer):
    def update(self, instances, validated_data):
        instance_hash = {index: instance for index, instance in enumerate(instances)}
        result = [
            self.child.update(instance_hash[index], attrs)
            for index, attrs in enumerate(validated_data)
        ]
        writable_fields = [
            x
            for x in self.child.Meta.fields
            if x not in self.child.Meta.read_only_fields
        ]
        try:
            self.child.Meta.model.objects.bulk_update(result, writable_fields)
        except IntegrityError as e:
            raise ValidationError(e)
        return result

class ActiveWorkingDaysSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    class Meta:
        fields = ['id','company', 'date', 'is_holiday']
        model = ActiveWorkingDays
        list_serializer_class = ActiveWorkingDaysListSerializer
        read_only_fields = ()


class TourplanSerializer(serializers.ModelSerializer):
    # select_the_date_id = serializers.ListField(child=serializers.CharField())
    purpose_of_visit = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    class Meta:
        model = TourPlan
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
    
class ShiftWiseTourplanSerializer(serializers.ModelSerializer):
    shift = ShiftSerializer(allow_null=True, required=False)
    tour_plan = TourplanSerializer()
    class Meta:
        model = ShiftWiseTourplan
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['shift'] = ShiftSerializer(instance.shift).data
        return response
    
    # def validate(self, attrs):
    #     if attrs['tour_plan']:
    #     return super().validate(attrs)


class ShiftWiseTourPlanSerializerForBulkCreate(serializers.ModelSerializer):
    tour_plan = TourplanSerializer(many=True)

    class Meta:
        model = ShiftWiseTourplan
        fields = '__all__'


class CompanyMPOAreaSerializers(serializers.ModelSerializer):

    class Meta:
        model = CompanyMPOArea
        fields = '__all__'
    
    def to_representation(self, instance):
        queryset = CompanyMPOArea.objects.select_related(
            'company_name',
            'mpo_name__company_name',
            'mpo_name__role_name__role_name',
            'mpo_name__role_name__company_name',
            'mpo_name__division_name',
            'mpo_name__executive_level',
            'mpo_name__company_area',
            'company_area')
        instance = queryset.get(pk=instance.pk)
        response = super().to_representation(instance)  
        response['mpo_name'] = CompanyUserRoleSerializers(
                                    instance.mpo_name).data     
        return response


# class CompanyMPODoctorSerializer(serializers.ModelSerializer):
#     doctor_name = DoctorSerializers()
#     class Meta:
#         model = CompanyMPODoctor
#         fields = '__all__'
#     def create(self, validated_data):
#         data = validated_data['doctor_name']
#         doctor_instance = Doctor(
#             doctor_name=data['doctor_name'],
#             doctor_address=data['doctor_area'],
#             doctor_gender=data['doctor_gender'],
#             doctor_phone_number=data['doctor_phone_number'],
#             doctor_territory=data['doctor_territory'],
#             doctor_category = data["doctor_category"],
#             doctor_nmc_number = data['doctor_nmc_number'],
#             doctor_qualification = data['doctor_qualification']
#         )
#         doctor_instance.save()
#         company_mpo_doctor_instance = CompanyMPODoctor(
#             company_name = validated_data['company_name'],
#             doctor_name = doctor_instance,
#             company_area = validated_data['company_area'],
#             mpo_name = validated_data['mpo_name']
#         )
#         company_mpo_doctor_instance.save()
#         return company_mpo_doctor_instance


class CompanyMPOAreaTourPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyMPOAreaTourPlan
        fields = "__all__"

    def to_representation(self, instance):
        # queryset = CompanyMPOAreaTourPlan.objects.select_related(
        #     'tour_plan_id',
        #     'company_mpo_area_id__company_name',
        #     'company_mpo_area_id__mpo_name',
        #     'company_mpo_area_id__company_area')
        # instance = queryset.get(pk=instance.pk)
        response = super().to_representation(instance)  
        response['company_mpo_area_id'] = CompanyMPOAreaSerializers(
                                    instance.company_mpo_area_id).data     
        return response



class CompanyMpoTourPlanSerializer(serializers.ModelSerializer):
    tour_plan = ShiftWiseTourplanSerializer()
    mpo_area = CompanyMPOAreaTourPlanSerializer(many=True, write_only=True,required=False)
    mpo_area_read = CompanyMPOAreaTourPlanSerializer(many=True, read_only=True,required=False)

    class Meta:
        model = CompanyMpoTourPlan
        fields = [
            'id',
            'mpo_area',
            'tour_plan',
            'mpo_name',
            'approved_by',
            'company_name',
            'mpo_area_read',
            'is_approved',
            'is_missed_call_calculated'
            ]

    def create(self, validated_data):
        shift_tour_plan = validated_data.get('tour_plan')
        tour_plan_data = shift_tour_plan['tour_plan']
        shift_data = shift_tour_plan['shift']
        if CompanyMpoTourPlan.objects.filter(
            tour_plan__tour_plan__select_the_date_id=tour_plan_data['select_the_date_id'],
            mpo_name=validated_data.get('mpo_name')).exists():
            raise serializers.ValidationError("Tour plan cant be multiple for same date")
        tour_plan_instance = TourPlan(
            select_the_month=tour_plan_data['select_the_month'],
            select_the_date_id=tour_plan_data['select_the_date_id'],
            purpose_of_visit=tour_plan_data['purpose_of_visit'],
            is_unplanned=tour_plan_data['is_unplanned'],
            is_admin_opened=tour_plan_data['is_admin_opened'],
            is_doctor_dcr_added=tour_plan_data['is_doctor_dcr_added'],
            is_chemist_dcr_added=tour_plan_data['is_chemist_dcr_added'],
            is_stockist_dcr_added=tour_plan_data['is_stockist_dcr_added'],
            hulting_station=tour_plan_data['hulting_station']
        )
        tour_plan_instance.save()
        tour_plan_area_mpo = [
            CompanyMPOAreaTourPlan(
                tour_plan_id=tour_plan_instance,
                company_mpo_area_id=area['company_mpo_area_id']) for area in validated_data['mpo_area']]
        CompanyMPOAreaTourPlan.objects.bulk_create(tour_plan_area_mpo)
        shift_instance = Shift.objects.get(id=shift_data['shift'])
        shift_wise_tour_plan_instance = ShiftWiseTourplan(
            tour_plan=tour_plan_instance,
            shift=shift_instance
        )
        shift_wise_tour_plan_instance.save()
        
        company_mpo_tour_plan=CompanyMpoTourPlan(
            mpo_name=validated_data.get('mpo_name'),
            tour_plan=shift_wise_tour_plan_instance,
            approved_by=validated_data.get('approved_by'),
            # submit_to = validated_data.get('submit_to'),
            company_name = validated_data.get('company_name')
        )
        if company_mpo_tour_plan.tour_plan.tour_plan.is_unplanned:
            CompanyMpoTourPlan.objects.filter(
                tour_plan__tour_plan__select_the_date_id=company_mpo_tour_plan.tour_plan.tour_plan.select_the_date_id
            ).delete()
        company_mpo_tour_plan.save()
        return company_mpo_tour_plan
    
    def update(self, instance, validated_data):
        shift_tour_plan = validated_data.get('tour_plan')
        tourplan_data = shift_tour_plan['tour_plan']
        shift_data = shift_tour_plan['shift']
        shift_wise_tour_plan_instance = instance.tour_plan
        tourplan_instance = shift_wise_tour_plan_instance.tour_plan
        if tourplan_data.get('select_the_date_id'):
            tourplan_instance.select_the_date_id = tourplan_data[
                'select_the_date_id']
        if tourplan_data.get('select_the_month'):
            tourplan_instance.select_the_month = tourplan_data[
                'select_the_month'
            ]
        if tourplan_data.get('purpose_of_visit'):
            tourplan_instance.purpose_of_visit = tourplan_data[
                'purpose_of_visit'
            ]
        if 'is_dcr_added' in tourplan_data and tourplan_data['is_dcr_added'] is not None:
            tourplan_instance.is_dcr_added = tourplan_data[
                'is_dcr_added'
            ]
        if 'is_unplanned' in tourplan_data and tourplan_data['is_unplanned'] is not None:
            tourplan_instance.is_unplanned = tourplan_data[
                'is_unplanned'
            ]

        if 'is_admin_opened' in tourplan_data and tourplan_data['is_admin_opened'] is not None:
            tourplan_instance.is_admin_opened = tourplan_data['is_admin_opened']

        if 'is_doctor_dcr_added' in tourplan_data and tourplan_data['is_doctor_dcr_added'] is not None:
            tourplan_instance.is_doctor_dcr_added = tourplan_data['is_doctor_dcr_added']
        
        if 'is_chemist_dcr_added' in tourplan_data and tourplan_data['is_chemist_dcr_added'] is not None:
            tourplan_instance.is_chemist_dcr_added = tourplan_data['is_chemist_dcr_added']

        if 'is_stockist_dcr_added' in tourplan_data and tourplan_data['is_stockist_dcr_added'] is not None:
            tourplan_instance.is_stockist_dcr_added = tourplan_data['is_stockist_dcr_added']

        if 'hulting_station' in tourplan_data and tourplan_data['hulting_station'] is not None:
            tourplan_instance.hulting_station = tourplan_data['hulting_station']
        
        tourplan_instance.save()
        if validated_data.get('mpo_area'):
            CompanyMPOAreaTourPlan.objects.filter(tour_plan_id=tourplan_instance.id).delete()
            company_mpo_area_tour_plan = [CompanyMPOAreaTourPlan(
                tour_plan_id=tourplan_instance,
                company_mpo_area_id=data.get('company_mpo_area_id'))
                for data in validated_data.get('mpo_area')]
            CompanyMPOAreaTourPlan.objects.bulk_create(company_mpo_area_tour_plan)

        if shift_data.get('shift') is not None:
            shift_instance = Shift.objects.get(id=shift_data['shift'])
            shift_wise_tour_plan_instance.tour_plan = TourPlan.objects.get(id=tourplan_instance.id)
            shift_wise_tour_plan_instance.shift=shift_instance
            shift_wise_tour_plan_instance.save()
            instance.tour_plan = shift_wise_tour_plan_instance
        if(validated_data.get('approved_by')):
            instance.approved_by = validated_data.get('approved_by')
        if(validated_data.get('is_approved')):
            instance.is_approved = validated_data.get('is_approved')
        instance.save()
        return instance
    
    def to_representation(self, instance):
        if hasattr(instance, '_cached_mpo_area'):
            return instance._cached_mpo_area
        if self.context['request'].method in ['POST', 'PATCH', 'PUT']:
            return super().to_representation(instance)
        response = super().to_representation(instance)
        response['company_name'] = CompanySerializers(
                                    instance.company_name).data   
        response['approved_by'] = CompanyUserRoleSerializers(
                                    instance.approved_by).data   
        response['mpo_name'] = CompanyUserRoleSerializers(
                                    instance.mpo_name).data
        response['mpo_area_read'] = CompanyMPOAreaTourPlanSerializer(
            CompanyMPOAreaTourPlan.objects.filter(
                tour_plan_id=instance.tour_plan.tour_plan.id), many=True).data
        instance._cached_mpo_area = response
        return response
    

class CompanyMPOTourPlanSerializer(serializers.Serializer):
    company_name = serializers.IntegerField()
    dates = serializers.CharField()
    mpo_name = serializers.IntegerField()
    purpose_of_visit = serializers.CharField()
    select_the_area = serializers.IntegerField()
    shift = serializers.IntegerField()

    def create(self, validated_data):
        shift_data = validated_data.get('shift')
        date_object = datetime.strptime(validated_data.get('dates'), '%Y-%m-%d')
        month_name = date_object.strftime('%B')
        tour_plan_data = TourPlan.objects.filter(select_the_date_id=validated_data.get('dates'))
        if tour_plan_data.count() >= 2:
            raise serializers.ValidationError("Can't create extra tour plan.")
        tour_plan_instance = TourPlan(
            select_the_month=month_name,
            select_the_date_id=validated_data.get('dates'),
            select_the_area=CompanyMPOArea.objects.get(id=validated_data.get('select_the_area')),
            purpose_of_visit=validated_data.get('purpose_of_visit'),
            is_unplanned=validated_data.get('is_unplanned'),
            hulting_station=validated_data.get('hulting_station')
        )
        tour_plan_instance.save()
        shift_instance = Shift.objects.get(id=shift_data)
        shift_wise_tour_plan_instance = ShiftWiseTourplan(
            tour_plan=tour_plan_instance,
            shift=shift_instance
        )
        shift_wise_tour_plan_instance.save()
        
        company_mpo_tour_plan=CompanyMpoTourPlan(
            mpo_name=CompanyUserRole.objects.get(id=validated_data.get('mpo_name')), 
            tour_plan=shift_wise_tour_plan_instance,
            approved_by=validated_data.get('approved_by'),
            # submit_to = validated_data.get('submit_to'),
            company_name = Company.objects.get(company_id=validated_data.get('company_name'))
        )
        company_mpo_tour_plan.save()
    