from nepali_date_converter import nepali_today
from datetime import datetime, date
from rest_framework import serializers
from Expenses.models import *
from Company.serializers import CompanyAreaSerializers
from DCRUser.serializers import CompanyUserRoleSerializers
from bsdate.convertor import BSDateConverter 


class ExpensesTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExpensesType
        fields = '__all__'


class CompanyAreaWiseExpensesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyAreaWiseExpeneses
        fields = '__all__'
    def create(self, validated_data):
        instance = CompanyAreaWiseExpeneses.objects.create(
            **validated_data
        )
        return instance 
    def update(self, instance, validated_data):
        return super().update(instance, validated_data) 
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        response['area_name'] = CompanyAreaSerializers(
            instance.area_name
        ).data
        return response


class LeaveApplicationSerializers(serializers.ModelSerializer):
    obj = BSDateConverter()
    class Meta:
        model = LeaveApplication
        fields = '__all__'

    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        response['leave_from'] = self.obj.convert_ad_to_bs(response['leave_from'])
        return response
    
    # def validate_leave_to(self, attrs):
    #     if attrs < date(nepali_today.year, nepali_today.month, nepali_today.day):
    #         raise serializers.ValidationError("Invalid leave to date")
    #     return attrs
    
    # def validate_leave_from(self, attrs):
    #     if attrs < date(nepali_today.year, nepali_today.month, nepali_today.day):
    #         raise serializers.ValidationError("Invalid leave from date")
    #     return attrs

class MpoWiseLeaveApplicationSerializers(serializers.ModelSerializer):
    application_id = LeaveApplicationSerializers()

    class Meta:
        model = MpoWiseLeaveApplication
        fields = '__all__'
    
    def create(self, validated_data):
        application_instance = LeaveApplication(
            **validated_data['application_id']
        )
        application_instance.save()
        mpo_wise_leave_application = MpoWiseLeaveApplication(
            mpo_name=validated_data['mpo_name'],
            application_id=application_instance
        )
        mpo_wise_leave_application.save()
        return mpo_wise_leave_application
    
    def update(self, instance, validated_data):
        application_data = validated_data['application_id']
        leave_application_instance = LeaveApplication.objects.get(id=instance.application_id.id)
        leave_application_instance.leave_type = application_data['leave_type']
        leave_application_instance.leave_cause = application_data['leave_cause']
        leave_application_instance.leave_from = application_data['leave_from']
        leave_application_instance.leave_to = application_data['leave_to']
        leave_application_instance.leave_status = application_data['leave_status']
        leave_application_instance.is_submitted = application_data['is_submitted']
        leave_application_instance.is_approved = application_data['is_approved']
        leave_application_instance.save()
        instance.application_id = leave_application_instance
        instance.save()
        return instance
    
    def to_internal_value(self, data):
        return super().to_internal_value(data)
    
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        response['mpo_name'] = CompanyUserRoleSerializers(instance.mpo_name).data
        return response
    
    def validate_application_id(self, attrs):
        converter = BSDateConverter()
        
        leave_from_bs = attrs['leave_from']
        leave_to_bs = attrs['leave_to']
        
        # Convert BS dates to AD dates
        # leave_from_ad = datetime.strptime(converter.convert_bs_to_ad(leave_from_bs), '%Y-%m-%d').date()
        # leave_to_ad = datetime.strptime(converter.convert_bs_to_ad(leave_to_bs), '%Y-%m-%d').date()
        
        # Get today's date in AD (Gregorian)
        nepali_today_ad = date.today()

        if not attrs['leave_cause']:
            raise serializers.ValidationError('Leave cause is mandatory.')
        if not leave_from_bs:
            raise serializers.ValidationError('Leave from date is mandatory.')
        if not leave_to_bs:
            raise serializers.ValidationError('Leave to date is mandatory.')

        # Check if the leave dates are before today
        if leave_from_bs < nepali_today_ad or leave_to_bs < nepali_today_ad:
            raise serializers.ValidationError('Invalid leave date: leave dates cannot be before today.')

        return attrs


class TargetSerializers(serializers.ModelSerializer):
    year = serializers.CharField(
        required=False,
        allow_null=True
    )
    target_amount = serializers.DecimalField(
        required=False,
        allow_null=True,
        max_digits=10,
        decimal_places=1
    )
    sales = serializers.DecimalField(
        required=False,
        allow_null=True,
        max_digits=10,
        decimal_places=1
    )
    # target_from = CompanyUserRoleSerializers(
    #     required=False,
    #     allow_null=True
    # )
    # target_to = CompanyUserRoleSerializers(
    #     required=False,
    #     allow_null=True
    # )
    class Meta:
        model = Target
        fields = '__all__'
    
    def create(self, validated_data):
        instance = Target(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        if validated_data['year']:
            instance.year = validated_data['year']
        if validated_data['target_amount']:
            instance.target_amount = validated_data['target_amount']
        if validated_data['sales']:
            instance.sales = validated_data['sales']
        if validated_data['target_from']:
            instance.target_from = validated_data['target_from']
        if validated_data['target_to']:
            instance.target_to = validated_data['target_to']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['target_from'] = CompanyUserRoleSerializers(
            instance.target_from).data
        response['target_to'] = CompanyUserRoleSerializers(
            instance.target_to).data
        return response


class UploadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uploads
        fields = '__all__'
    
    def create(self, validated_data):
        instance = Uploads(**validated_data)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.mpo_name = validated_data['mpo_name']
        instance.upload_type = validated_data['upload_type']
        instance.upload = validated_data['upload']
        instance.upload_name = validated_data['upload_name']
        instance.save()
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mpo_name'] = CompanyUserRoleSerializers(
            instance.mpo_name
        ).data
        return response
    

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseData
        fields = '__all__'