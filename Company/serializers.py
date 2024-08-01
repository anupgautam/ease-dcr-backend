from rest_framework import serializers
from Company.models import (
    Company,
    CompanyHolidayArea,
    CompanyHolidayDate,
    Roles,
    WorkingHour,
    Division,
    CompanyArea,
    CompanyRoles,
    CompanyWiseDivision,
    CompanyWorkingHour,
    CompanyNotices,
    CompanySalaryRoles,
    CompanyHoliday,
)
from Company.models import Notices
from rest_framework.response import Response


class CompanySerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False, allow_null=True)
    company_address = serializers.CharField(required=False, allow_null=True)
    company_email_address = serializers.EmailField(required=False, allow_null=True)

    class Meta:
        model = Company
        fields = "__all__"


class RolesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = "__all__"


class NoticeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Notices
        fields = "__all__"


class WorkingHourSerializers(serializers.ModelSerializer):
    class Meta:
        model = WorkingHour
        fields = "__all__"


class DivisionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = "__all__"


class CompanyAreaSerializers(serializers.ModelSerializer):
    # id = serializers.IntegerField(allow_null=True, required=False)
    class Meta:
        model = CompanyArea
        fields = "__all__"

    def create(self, validated_data):
        company_area_instance = CompanyArea(
            company_name=validated_data["company_name"],
            company_area=validated_data["company_area"],
            station_type=validated_data["station_type"],
        )
        company_area_instance.save()
        return company_area_instance

    def update(self, instance, validated_data):
        # area_instance = WorkingArea.objects.get(id=instance.company_area.id)
        # if(validated_data.get('company_area')['latitude']):
        #     area_instance.latitude = validated_data['company_area']['latitude']
        # if(validated_data.get('company_area')['longitude']):
        #     area_instance.longitude = validated_data['company_area']['longitude']
        # if(validated_data.get('company_area')['country']):
        #     area_instance.country = validated_data['company_area']['country']
        # if(validated_data.get('company_area')['state']):
        #     area_instance.state = validated_data['company_area']['state']
        # if(validated_data.get('company_area')['division']):
        #     area_instance.division = validated_data['company_area']['division']
        # if(validated_data.get('company_area')['area_name']):
        #     area_instance.area_name = validated_data['company_area']['area_name']
        # area_instance.save()
        instance.company_area = validated_data.get("company_area")
        instance.station_type = validated_data.get("station_type")
        instance.save()
        return instance


class CompanyAreaSerializersWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = CompanyArea
        fields = "__all__"


class CompanyAreaSerializersWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = CompanyArea
        fields = "__all__"


class CompanyRolesSerializersWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = CompanyRoles
        fields = ["id", "company_name", "role_name", "priority_value"]


class CompanyRolesSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = CompanyRoles
        fields = [
            "id",
            "company_name",
            "role_name",
            "priority_value",
            "role_name_value",
        ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if isinstance(instance, dict):
            response["role_name"] = RolesSerializers(instance["role_name"]).data
        else:
            response["role_name"] = RolesSerializers(instance.role_name).data
        return response


class CompanyWorkingHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyWorkingHour
        fields = "__all__"


class CompanyWiseDivisionSerializers(serializers.ModelSerializer):
    # division_name = DivisionSerializers()
    class Meta:
        model = CompanyWiseDivision
        fields = "__all__"


class CompanyNoticeSerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyNotices
        fields = "__all__"


class NoticeAddSerializers(serializers.ModelSerializer):
    company_name = serializers.CharField(max_length=100)

    class Meta:
        model = Notices
        fields = ["notice_name", "company_name", "notice_description"]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return Notices.objects.create_notice_using_signal(
            notice_name=validated_data["notice_name"],
            notice_description=validated_data["notice_description"],
            company_name=validated_data["company_name"],
        )


class CompanyRoleSalarySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CompanySalaryRoles

    def create(self, validated_data):
        company_salary_role_instance = CompanySalaryRoles.objects.create(
            **validated_data
        )
        company_salary_role_instance.save()
        return company_salary_role_instance

    def update(self, instance, validated_data):
        instance.company_name = validated_data["company_name"]
        instance.company_roles = validated_data["company_roles"]
        instance.salary = validated_data["salary"]
        instance.save()
        return instance


class CompanyHolidaySerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CompanyHoliday


class CompanyHolidayAreaSerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CompanyHolidayArea


class CompanyHolidayDateSerializers(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = CompanyHolidayDate
