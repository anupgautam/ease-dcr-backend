from rest_framework import viewsets
from rest_framework import status

from Mpo.utils import general_notification_send, get_upper_level_user_id, get_user_id, get_user_name
from .models import HigherOrderTourPlanVisit, HigherOrderTourplan, HigherOrderDCR
from .serializers import HigherOrderTourplanSerializer, HigherOrderDcrSerializer
from rest_framework.response import Response
from .utils import data_transmission, update_data_transmission, dcr_data_transmission
from django_filters.rest_framework import DjangoFilterBackend
from Account.pagination import CustomPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.permissions import *
from datetime import datetime, timedelta
from Company.models import CompanyRolesTPLock
from DCRUser.models import CompanyUserRole
from datetime import date
from rest_framework.decorators import action
from nepali_date_converter import nepali_today
from bsdate.convertor import BSDateConverter


class HigherOrderTourplanViewset(viewsets.ModelViewSet):
    queryset = HigherOrderTourplan.objects.all()
    serializer_class = HigherOrderTourplanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "date",
        "user_id",
        "month",
        "year",
        "is_dcr_added",
        "is_unplanned",
        "is_approved",
        "shift",
        "user_id__role_name",
    ]

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request
    #     return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("date")

    def create(self, request, *args, **kwargs):
        data = data_transmission(request)
        serializer = self.serializer_class(
            data=data, many=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            general_notification_send(
                {
                    'type':"Higher Order Tourplan",
                    "receiver_id":get_upper_level_user_id(data[0]['user_id']),
                    "sender_name":get_user_name(data[0]['user_id']),
                    "url":"",
                    "sender_id":get_user_id(data[0]['user_id']),
                    "notification_title":"Tourplan Created",
                    "notification_description":f"{get_user_name(data[0]['user_id'])} has succesfully created Tourplan"
                }
            )
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = HigherOrderTourplan.objects.get(id=kwargs.get("pk"))
        data = update_data_transmission(request)
        serializer = self.serializer_class(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            HigherOrderTourPlanVisit.objects.filter(
                higher_order_tour_plan_id=instance.id
            ).delete()
            tour_plan_visit = [
                HigherOrderTourPlanVisit(
                    visited_with=data.get('visited_with'),
                    # area=data.get('area'),
                    higher_order_tour_plan_id=serializer.data[0].id)
                    for data in request.data.get('visit_data')
                    ]
            HigherOrderTourPlanVisit.objects.bulk_create(tour_plan_visit)
            general_notification_send(
                {
                    'type':"Higher Order Tourplan",
                    "receiver_id":get_upper_level_user_id(data['user_id']),
                    "sender_name":get_user_name(data['user_id']),
                    "url":"",
                    "sender_id":get_user_id(data['user_id']),
                    "notification_title":"Tourplan Updated",
                    "notification_description":f"{get_user_name(data['user_id'])} has updated Tourplan"
                }
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def get_higher_order_missed_tourplans(self, request):
        today = date.today()
        tour_plans_before_today = HigherOrderTourplan.objects.filter(
            user_id=request.data.get("user_id"),
            date__lt=today,
            is_dcr_added=False,
            is_approved=True,
        )
        serializer = self.serializer_class(
            tour_plans_before_today, many=True, context={"request": request}
        )
        return JsonResponse(serializer.data, safe=False)

    @action(detail=False, methods=["GET"])
    def get_tour_plan(self, request):
        company_user_role = CompanyUserRole.objects.get(id=request.GET.get("user_id"))
        if company_user_role.is_tp_locked:
            return Response(
                data={"status": "Your user has been locked"}, status=status.HTTP_200_OK
            )

        if self.is_locked_tour_plan(request):
            company_user_role.is_tp_locked = True
            company_user_role.save()
            self.is_locked_tour_plan_mpo(is_locked=True)

            return Response(
                data={"status": "Your user has been locked"}, status=status.HTTP_200_OK
            )
        tour_plan_list = HigherOrderTourplan.objects.filter(
            Q(
                date__in=[
                    date(nepali_today.year, nepali_today.month, nepali_today.day),
                    date(nepali_today.year, nepali_today.month, nepali_today.day - 1),
                    date(nepali_today.year, nepali_today.month, nepali_today.day - 2),
                ]
            )
            | Q(is_admin_opened=True),
            user_id=request.GET.get("user_id"),
            is_approved=True,
        )
        serializer = HigherOrderTourplanSerializer(
            tour_plan_list, many=True, context={"request": request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def is_locked_tour_plan(self, request, is_locked=False):
        company_lock_day = CompanyRolesTPLock.objects.get(
            company_roles=CompanyUserRole.objects.get(
                id=request.GET.get("user_id")
            ).role_name
        ).tp_lock_days
        latest_date_list = [
            date(nepali_today.year, nepali_today.month, nepali_today.day - day)
            for day in range(1, company_lock_day + 1)
        ]
        tour_plan_list = HigherOrderTourplan.objects.filter(
            ~Q(date__in=latest_date_list),
            is_dcr_added=False,
            user_id=request.GET.get("user_id"),
            is_approved=True,
            is_admin_opened=False,
            date__lte=date(nepali_today.year, nepali_today.month, nepali_today.day),
        )
        if is_locked:
            tour_plan_list.update(is_locked=True)
            return {}
        return len(tour_plan_list) == company_lock_day

    @action(detail=False, methods=["GET"])
    def get_locked_tour_plan_list(self, request):
        tour_plan_list = HigherOrderTourplan.objects.filter(
            ~Q(
                date__in=[
                    date(nepali_today.year, nepali_today.month, nepali_today.day),
                    date(nepali_today.year, nepali_today.month, nepali_today.day - 1),
                    date(nepali_today.year, nepali_today.month, nepali_today.day - 2),
                ]
            ),
            is_dcr_added=False,
            user_id=request.GET.get("user_id"),
            is_approved=True,
            is_admin_opened=False,
            date__lte=date(nepali_today.year, nepali_today.month, nepali_today.day),
        )
        serializer = HigherOrderTourplanSerializer(
            tour_plan_list, many=True, context={"request": request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class HigherOrderTourplanViewsetWithPagination(viewsets.ModelViewSet):
    queryset = HigherOrderTourplan.objects.all()
    serializer_class = HigherOrderTourplanSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "date",
        "user_id",
        "month",
        "year",
        "visited_with__company_name",
        "user_id__role_name",
    ]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("date")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class HigherOrderDcrWithPagination(viewsets.ModelViewSet):
    queryset = HigherOrderDCR.objects.exclude(user_id__user_name__is_active=False)
    serializer_class = HigherOrderDcrSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "date",
        "user_id",
        "month",
        "year",
        "user_id__role_name",
        "company_id",
    ]


class HigherOrderDcrViewset(viewsets.ModelViewSet):
    queryset = HigherOrderDCR.objects.all()
    serializer_class = HigherOrderDcrSerializer
    filterset_fields = ["user_id__role_name", "year", "month", "date"]

    def create(self, request, *args, **kwargs):
        data = dcr_data_transmission(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        instance = HigherOrderDCR.objects.get(id=kwargs.get("pk"))
        data = dcr_data_transmission(request)
        serializer = self.serializer_class(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(["post"])
@permission_classes((IsAuthenticated,))
def tour_plan_bulk_update_by_month(request):
    if (
        request.data.get("month")
        and request.data.get("year")
        and request.data.get("user_id")
    ):
        HigherOrderTourplan.objects.filter(
            month=request.data.get("month"),
            year=request.data.get("year"),
            user_id=request.data.get("user_id"),
        ).update(is_approved=True, approved_by=request.data.get("approved_by"))
        return Response("updated successfully")
    else:
        return Response("Please send all the fields")


@api_view(["POST"])
def get_the_other_roles_tourplan_of_30_days(request):
    current_date = datetime.now()
    new_date = current_date + timedelta(days=30)
    new_date_string = new_date.strftime("%Y-%m-%d")
    company_mpo_tour_plan_list = HigherOrderTourplan.objects.filter(
        Q(user_id__id=request.data.get("id"))
        & Q(date__range=(current_date.strftime("%Y-%m-%d"), new_date_string))
    )
    serializer = HigherOrderTourplanSerializer(
        company_mpo_tour_plan_list, many=True, context={"request": request}
    )
    return JsonResponse(
        serializer.data,
        status=200,
        headers={"content_type": "application/json"},
        safe=False,
    )
