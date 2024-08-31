# from asyncore import write
import datetime
from nepali_datetime import date
from logging.config import valid_ident
from collections import OrderedDict

from django.db.models import Q

from Mpo.models import CompanyMpoTourPlan
from rest_framework import serializers

from DCRUser.models import (
    User,
    CompanyUser,
    CompanyUserRole,
)
from Company.serializers import (
    CompanyAreaSerializers,
    CompanySerializers,
    RolesSerializers,
)
from Company.models import Company, Roles
from DCRUser.models import *
from Account.serializers import *
from Company.serializers import CompanyRolesSerializers, CompanyWiseDivisionSerializers
from DCRUser.utils import month_number_to_name


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CompanyUserSerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CompanyUser

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["company_name"] = CompanySerializers(instance.company_name).data
        response["user_name"] = UserSerializers(instance.user_name).data
        return response

    def update(self, instance, validated_data, partial=True):
        return super().update(instance, validated_data)


class AddCompanyUserSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200, write_only=True)
    last_name = serializers.CharField(max_length=200, write_only=True)
    address = serializers.CharField(max_length=200, write_only=True)
    contact_number = serializers.CharField(max_length=20, write_only=True)
    email = serializers.EmailField(write_only=True)
    role_name = serializers.CharField(max_length=20, write_only=True)
    date_of_joining = serializers.DateField(write_only=True)

    class Meta:
        model = CompanyUser
        fields = "__"

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return CompanyUser.objects.create_company_user_role(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            address=validated_data["address"],
            contact_number=validated_data["contact_number"],
            email=validated_data["email"],
            role_name=validated_data["role_name"],
            date_of_joining=validated_data["date_of_joining"],
        )


class CompanyUserRoleSerializersWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = CompanyUserRole
        fields = "__all__"


class CompanyUserRoleSerializers(serializers.ModelSerializer):
    # company_name = CompanySerializers()
    # role_name = CompanyRolesSerializers(required=False,
    #                                     allow_null=True)
    user_name = UserSerializers(required=False, allow_null=True)
    dcr_pending = serializers.IntegerField(read_only=True)
    dcr_feeded = serializers.IntegerField(read_only=True)
    # division_name = CompanyWiseDivisionSerializers()

    class Meta:
        model = CompanyUserRole
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.get("user_name")
        # role_name = validated_data.get('role_name')
        company = validated_data.get("company_name")
        company_instance = Company.objects.get(company_id=company.company_id)
        # company_user_role_instance = CompanyRoles.objects.get(role_name=role_name['role_name'],company_name=company)
        user_model = User(
            first_name=user["first_name"],
            last_name=user["last_name"],
            middle_name=user["middle_name"],
            email=user["email"],
            phone_number=user["phone_number"],
            date_of_joining=user["date_of_joining"],
            is_active=True,
        )
        user_model.set_password("12345")
        user_model.save()
        company_user = CompanyUser.objects.create(
            user_name=user_model, company_name=company_instance
        )
        company_user.save()
        company_user_role = CompanyUserRole.objects.create(
            user_name=user_model,
            role_name=validated_data["role_name"],
            company_name=company_instance,
            division_name=validated_data["division_name"],
            executive_level=validated_data["executive_level"],
            company_area=validated_data["company_area"],
            station_type=validated_data["station_type"],
        )
        company_user_role.save()
        return company_user_role

    def update(self, instance, validated_data, partial=True):
        company = validated_data.get("company_name")
        user = validated_data.get("user_name")
        role = validated_data.get("role_name")
        # company = validated_data.get('company_name')
        email = user["email"]
        if email == "xyz@gmail.com":
            email = instance.user_name.email
        user_object = User.objects.get(email=instance.user_name.email)
        user_object.first_name = user["first_name"]
        user_object.last_name = user["last_name"]
        user_object.middle_name = user["middle_name"]
        user_object.email = email
        user_object.phone_number = user["phone_number"]
        user_object.date_of_joining = user["date_of_joining"]
        user_object.is_active = user["is_active"]
        # user_object.address = user['address']
        user_object.save()
        # role_object = CompanyRoles.objects.get(role_name=role['role_name'], company_name=company)
        # division_object = CompanyWiseDivision.objects.get(division_name=division['division_name'], company_name=company['company_name'])
        # company_object= Company.objects.get(company_id=company['company_name'])
        instance.user_name = user_object
        instance.role_name = validated_data["role_name"]
        instance.division_name = validated_data["division_name"]
        instance.executive_level = validated_data["executive_level"]
        instance.company_name = validated_data["company_name"]
        instance.company_area = validated_data["company_area"]
        instance.station_type = validated_data["station_type"]
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if isinstance(instance, OrderedDict):
            # Access the necessary fields from the OrderedDict if needed
            company_name = instance.get("company_name")
            role_name = instance.get("role_name")
            company_area = instance.get("company_area")
            executive_level = instance.get("executive_level")
            division_name = instance.get("division_name")
        else:
            print(instance)
            company_name = instance.company_name
            role_name = instance.role_name
            company_area = instance.company_area
            executive_level = instance.executive_level
            division_name = instance.division_name
        response["company_name"] = CompanySerializers(company_name).data
        response["role_name"] = CompanyRolesSerializers(role_name).data
        response["company_area"] = CompanyAreaSerializers(company_area).data
        response["executive_level"] = CompanyUserSerializers(executive_level).data
        response["division_name"] = CompanyWiseDivisionSerializers(division_name).data
        tour_plan_list = CompanyMpoTourPlan.objects.filter(
            mpo_name=instance,
            tour_plan__tour_plan__select_the_month=month_number_to_name[
                date.today().month
            ],
        ).count()
        tour_plan_dcr_list = CompanyMpoTourPlan.objects.filter(
            Q(mpo_name=instance)
            & Q(
                tour_plan__tour_plan__select_the_month=month_number_to_name[
                    date.today().month
                ]
            )
            & (
                Q(tour_plan__tour_plan__is_dcr_added=True)
                | Q(tour_plan__tour_plan__is_chemist_dcr_added=True)
                | Q(tour_plan__tour_plan__is_stockist_dcr_added=True)
                | Q(tour_plan__tour_plan__is_doctor_dcr_added=True)
            )
        ).count()
        response["dcr_pending"] = tour_plan_list - tour_plan_dcr_list
        response["dcr_feeded"] = tour_plan_dcr_list
        return response


class CompanyUserAttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyUserAttendance
        fields = "__all__"
