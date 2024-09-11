from Mpo.models import CompanyMPOArea
from rest_framework import serializers

from dailycallrecord.utils import nepali_month_from_english
from .models import HigherOrderTourPlanVisit, HigherOrderTourplan, HigherOrderDCR
from DCRUser.serializers import CompanyUserRoleSerializers
from Mpo.serializers import ShiftSerializer
from Company.serializers import CompanySerializers
from DCRUser.models import CompanyUserRole
from datetime import datetime


class HigherOrderTourPlanWriteOnlySerializer(serializers.Serializer):
    visited_with = serializers.CharField()
    area = serializers.CharField()

    def to_representation(self, instance):
        # Always return an empty dictionary for representation
        return {}
    
class HigherOrderTourPlanVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HigherOrderTourPlanVisit
        fields = '__all__'

    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['visited_with_name'] = CompanyMPOArea.objects.get(instance.id).mpo_name.user_name.first_name
    #     return response

        
class HigherOrderTourplanSerializer(serializers.ModelSerializer):
    visit_data = HigherOrderTourPlanVisitSerializer(many=True, write_only=True)
    visited_data = HigherOrderTourPlanVisitSerializer(many=True, read_only=True)
    date = serializers.DateField(
        required=False,
        allow_null=True
    )
    is_dcr_added = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    is_approved = serializers.BooleanField(
        required=False,
        allow_null=True
    )
    is_unplanned = serializers.BooleanField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = HigherOrderTourplan
        fields = '__all__'

    def create(self, validated_data):
        if HigherOrderTourplan.objects.filter(
            date=validated_data.get('date'),
            user_id=validated_data.get('user_id'),
            company_id=validated_data.get('company_id')).count()>=1 and not validated_data.get('is_unplanned'):
            raise serializers.ValidationError("Tour plan can't be multiple for same date.")
        data = validated_data.copy()
        visit_data = data.pop('visit_data')
        if validated_data.get('is_unplanned'):
            HigherOrderTourplan.objects.filter(date=validated_data.get('date')).delete()
        instance = HigherOrderTourplan.objects.create(**data)
        tour_plan_visit = [
                HigherOrderTourPlanVisit(
                    visited_with=data.get('visited_with'),
                    # area=data.get('area'),
                    high_order_tour_plan_id=instance)
                    for data in validated_data.get('visit_data')
                    ]
        HigherOrderTourPlanVisit.objects.bulk_create(tour_plan_visit)
        validated_data['visit_data'] = visit_data
        return validated_data
    
    def update(self, instance, validated_data):
        # data = validated_data
        if validated_data.get('date'):
            date = validated_data['date']
            instance.date = date
            # month_year = datetime.strptime(validated_data.get('date'),"%Y-%m-%d")
            instance.month = nepali_month_from_english(date.strftime("%B"))
            instance.year = date.year
        if validated_data.get('company_id'):
            instance.company_id = validated_data['company_id']
        if validated_data.get('user_id'):   
            instance.user_id = validated_data['user_id']
        if validated_data.get('approved_by'):
            instance.approved_by = validated_data['approved_by']
        if validated_data.get('is_approved'):
            instance.is_approved = validated_data['is_approved']
        if validated_data.get('shift'):
            instance.shift = validated_data['shift']
        if validated_data.get('is_dcr_added') is not None and 'is_dcr_added' in validated_data:
            instance.is_dcr_added = validated_data['is_dcr_added']
        if validated_data.get('is_unplanned'):
            instance.is_unplanned = validated_data['is_unplanned']
        if validated_data.get('hulting_station'):
            instance.hulting_station = validated_data['hulting_station']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        if self.context['request'].method == 'POST':
            return super().to_representation(instance)
        response = super().to_representation(instance)
        response['visited_data'] = HigherOrderTourPlanVisitSerializer(
            HigherOrderTourPlanVisit.objects.filter(
                high_order_tour_plan_id=instance.id), many=True).data
        # response['shift'] = ShiftSerializer(
        #     instance.shift
        # ).data
        response['user_id'] = CompanyUserRoleSerializers(
            instance.user_id
        ).data
        return response
    

class HigherOrderDcrSerializer(serializers.ModelSerializer):
    class Meta:
        model = HigherOrderDCR
        fields = '__all__'
    def create(self, validated_data):
        instance = HigherOrderDCR.objects.create(**validated_data)
        return instance
    
    def update(self, instance, validated_data):
        instance.date = validated_data['date']
        instance.visited_with = validated_data['visited_with']
        instance.company_id = validated_data['company_id']
        instance.user_id = validated_data['user_id']
        instance.shift = validated_data['shift']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['visited_with'] = CompanyUserRoleSerializers(
            instance.visited_with
        ).data
        response['shift'] = ShiftSerializer(
            instance.shift
        ).data
        response['user_id'] = CompanyUserRoleSerializers(
            instance.user_id
        ).data
        return response