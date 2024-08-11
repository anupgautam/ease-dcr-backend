from rest_framework import viewsets
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from Doctors.utils import get_user_from_access
from .utils import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from Company.serializers import (
    CompanyHolidayDateSerializers,
    CompanyRolesTPLockSerializers,
    CompanySerializers,
    DivisionSerializers,
    RolesSerializers,
    NoticeSerializers,
    WorkingHourSerializers,
    CompanyWiseDivisionSerializers,
    CompanyNoticeSerializers,
    CompanyAreaSerializers,
    CompanyAreaSerializersWithoutToRepresentation,
    CompanyWorkingHourSerializer,
    CompanyRolesSerializers,
    NoticeAddSerializers,
    CompanyRoleSalarySerializer,
    CompanyHolidaySerializers,
    CompanyHolidayAreaSerializers,
)
from Company.models import (
    Company,
    CompanyHolidayDate,
    CompanyRolesTPLock,
    Division,
    Roles,
    Notices,
    WorkingHour,
    CompanyWiseDivision,
    CompanyNotices,
    CompanyWorkingHour,
    CompanyRoles,
    CompanySalaryRoles,
    CompanyHoliday,
    CompanyHolidayArea,
    CompanyArea,
)


class CompanyViewset(viewsets.ModelViewSet):
    model = Company
    queryset = Company.objects.all()
    serializer_class = CompanySerializers


class DivisionViewset(viewsets.ModelViewSet):
    model = Division
    queryset = Division.objects.all()
    serializer_class = DivisionSerializers


class RolesViewset(viewsets.ModelViewSet):
    model = Roles
    queryset = Roles.objects.all()
    serializer_class = RolesSerializers


class NoticesViewset(viewsets.ModelViewSet):
    model = Notices
    queryset = Notices.objects.all()
    serializer_class = NoticeSerializers


# class WorkingAreaViewset(viewsets.ModelViewSet):
#     model = WorkingArea
#     queryset = WorkingArea.objects.all()
#     serializer_class = WorkingAreaSerializers


class WorkingHourViewset(viewsets.ModelViewSet):
    model = WorkingHour
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializers


class CompanyWiseDivsionViewset(viewsets.ModelViewSet):
    model = CompanyWiseDivision
    queryset = CompanyWiseDivision.objects.all()
    serializer_class = CompanyWiseDivisionSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]


class CompanyNoticesViewset(viewsets.ModelViewSet):
    model = CompanyNotices
    queryset = CompanyNotices.objects.all()
    serializer_class = CompanyNoticeSerializers


class CompanyAreaViewset(viewsets.ModelViewSet):
    model = CompanyArea
    queryset = CompanyArea.objects.all()
    serializer_class = CompanyAreaSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     data = company_area_crud_data_transmission(request)
    #     serializer = self.serializer_class(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     instance = CompanyArea.objects.get(id=kwargs.get('pk'))
    #     data = company_area_crud_data_transmission(request)
    #     serializer = self.serializer_class(instance, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyAreaViewsetWithoutToRepresentation(viewsets.ModelViewSet):
    model = CompanyArea
    queryset = CompanyArea.objects.all()
    serializer_class = CompanyAreaSerializersWithoutToRepresentation
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]


class CompanyWorkingHourViewset(viewsets.ModelViewSet):
    model = CompanyWorkingHour
    queryset = CompanyWorkingHour.objects.all()
    serializer_class = CompanyWorkingHourSerializer


class CompanyRolesViewset(viewsets.ModelViewSet):
    model = CompanyRoles
    queryset = CompanyRoles.objects.all()
    serializer_class = CompanyRolesSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(role_name__role_name="admin")




class NoticeViewset(viewsets.ModelViewSet):
    queryset = Notices.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid()
            serializer.save()
        except Exception as e:
            pass
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == "create":
            return NoticeAddSerializers
        else:
            return NoticeSerializers


class CompanyRolesSalaryViewset(viewsets.ModelViewSet):
    queryset = CompanySalaryRoles.objects.all()
    serializer_class = CompanyRoleSalarySerializer

    def create(self, request, *args, **kwargs):
        company = get_user_from_access(request.data.get("access"))
        data = company_role_salary_data_transmission(request, company["company_name"])
        print(data)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        company = get_user_from_access(request.data.get("access"))
        instance = CompanySalaryRoles.objects.get(id=id)
        data = company_role_salary_data_transmission(request, company["company_name"])
        serializer = self.serializer_class(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class CompanyHolidayViewset(viewsets.ModelViewSet):
    model = CompanyHoliday
    queryset = CompanyHoliday.objects.all()
    serializer_class = CompanyHolidaySerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CompanyHolidayAreaViewset(viewsets.ModelViewSet):
    model = CompanyHolidayArea
    queryset = CompanyHolidayArea.objects.all()
    serializer_class = CompanyHolidayAreaSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_area", "holiday_type__holiday_name","company_area__company_name"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def bulk_create_company_holiday(self, request):
        company_area = request.data.get("company_area")
        holiday_type = request.data.get("holiday_type")
        company_holiday_area = [
            CompanyHolidayArea(
                company_area=CompanyArea.objects.get(id=comp_area),
                holiday_type=CompanyHoliday.objects.get(id=holiday_type))
            for comp_area in company_area
            if not CompanyHolidayArea.objects.get(
                company_area__id=comp_area,
                holiday_type__id=holiday_type)
        ]
        CompanyHolidayArea.objects.bulk_create(company_holiday_area)
        return Response(
            data={"Success": "Successfully created company holiday area"},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["patch"])
    @permission_classes(
        [
            IsAuthenticated,
        ]
    )
    def bulk_update_company_holiday(self, request):
        holiday_type = request.data.get("holiday_type")
        company_area = request.data.get("company_area")
        CompanyHolidayArea.objects.filter(holiday_type__id=holiday_type).delete()
        company_holiday_area = [
            CompanyHolidayArea(
                company_area=CompanyArea.objects.get(id=comp_area),
                holiday_type=CompanyHoliday.objects.get(id=holiday_type))
            for comp_area in company_area
            if not CompanyHolidayArea.objects.get(
                company_area__id=comp_area,
                holiday_type__id=holiday_type)
        ]
        CompanyHolidayArea.objects.bulk_create(company_holiday_area)
        return Response(
            data={"Success": "Successfully created company holiday area"},
            status=status.HTTP_200_OK,
        )


class CompanyHolidayDateViewset(viewsets.ModelViewSet):
    model = CompanyHolidayDate
    queryset = CompanyHolidayDate.objects.all()
    serializer_class = CompanyHolidayDateSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    

class CompanyRolesTPLockViewset(viewsets.ModelViewSet):
    model = CompanyRolesTPLock
    queryset = CompanyRolesTPLock.objects.all()
    serializer_class = CompanyRolesTPLockSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_roles"]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
