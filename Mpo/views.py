from datetime import date, datetime, timedelta

from django.db.models import Q
from django.http import JsonResponse

# from query_counter.decorators import queries_counter
from django_filters.rest_framework import DjangoFilterBackend
from nepali_date_converter import nepali_today
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from Account.pagination import CustomPagination
from Chemist.models import CompanyWiseChemist
from Company.models import CompanyRolesTPLock
from dailycallrecord.utils import nepali_month_to_digit
from DCRUser.models import CompanyUserRole
from DCRUser.serializers import CompanyUserRoleSerializers
from Doctors.models import CompanyWiseDoctor


# from Mpo.serializers import *
from Mpo.models import (
    ActiveWorkingDays,
    CompanyDivisionWiseMpo,
    CompanyMPOArea,
    CompanyMpoTourPlan,
    PurposeOfVisit,
    Shift,
    ShiftWiseTourplan,
    TourPlan,
)
from Mpo.serializers import (
    ActiveWorkingDaysSerializer,
    CompanyDivisionWiseMpoSerializer,
    CompanyMPOAreaSerializers,
    CompanyMpoTourPlanSerializer,
    PurposeOfVisitSerializer,
    ShiftSerializer,
    ShiftWiseTourplanSerializer,
    TourplanSerializer,
)
from Mpo.utils import (
    mpo_update_data_transmission,
)

from .backends import CaseInsensitiveDjangoFilterBackend
from .utils import (
    datetime_string,
    get_next_month,
    get_next_month_date,
    get_year_month_from_date,
)


class ShiftViewset(viewsets.ModelViewSet):
    model = Shift
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer


class CompanyDivisionwiseMpoViewset(viewsets.ModelViewSet):
    # model = CompanyDivisionWiseMpo
    queryset = CompanyDivisionWiseMpo.objects.select_related(
        "mpo_name__company_name",
        "mpo_name__user_name",
        "mpo_name__role_name",
        "mpo_name__executive_level",
        "division_name",
        "company_name",
    )
    serializer_class = CompanyDivisionWiseMpoSerializer


class PurposeofVisitViewset(viewsets.ModelViewSet):
    model = PurposeOfVisit
    queryset = PurposeOfVisit.objects.all()
    serializer_class = PurposeOfVisitSerializer


class ActiveWorkingDaysViewset(ListCreateAPIView):
    model = ActiveWorkingDays
    queryset = ActiveWorkingDays.objects.all()
    serializer_class = ActiveWorkingDaysSerializer

    def create(self, request, *args, **kwargs):
        date = request.data.get("date")
        serializer = ActiveWorkingDaysSerializer(data=date, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def validate_dates(data, field="date", unique=True):
    if isinstance(data, list):
        date_list = [datetime_string(x[field]) for x in data]

        if unique and len(date_list) != len(set(date_list)):
            raise ValidationError("Multiple updates to a single {} found".format(field))

        return date_list
    return [data]


class WorkingDaysViewset(viewsets.ModelViewSet):
    model = ActiveWorkingDays
    queryset = ActiveWorkingDays.objects.all()
    serializer_class = ActiveWorkingDaysSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company", "date", "is_holiday"]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)

    def get_queryset(self, company_id=None, dates=None):
        if company_id and dates:
            return ActiveWorkingDays.objects.filter(
                company_id=company_id, date__date__in=dates
            )
        return super().get_queryset()

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def bulk_update_company_date(self, request, *args, **kwargs):
        dates = validate_dates(request.data)
        instances = self.get_queryset(
            company_id=request.data[0].get("company"), dates=dates
        )
        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def monthly_holiday(self, request, *args, **kwargs):
        active_working_days = ActiveWorkingDays.objects.filter(
            company=request.data.get("company_name"),
            is_holiday=True,
            date__month=nepali_month_to_digit(request.data.get("month")),
            date__year=request.data.get("year"),
        )
        serializers = self.serializer_class(active_working_days, many=True)
        return Response(serializers.data)


class TourPlanViewset(viewsets.ModelViewSet):
    model = TourPlan
    queryset = TourPlan.objects.all()
    serializer_class = TourplanSerializer


class ShiftWiseTourplanViewset(viewsets.ModelViewSet):
    model = ShiftWiseTourplan
    queryset = ShiftWiseTourplan.objects.select_related("shift", "tour_plan").all()
    serializer_class = ShiftWiseTourplanSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("tour_plan__select_the_date_id")


class CompanyMPOAreaViewset(viewsets.ModelViewSet):
    model = CompanyMPOArea
    queryset = CompanyMPOArea.objects.exclude(mpo_name__user_name__is_active=False)
    serializer_class = CompanyMPOAreaSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["id", "company_name", "mpo_name", "company_area"]


class CompanyMpoTourplanWithOutPagination(viewsets.ModelViewSet):
    model = CompanyMpoTourPlan
    queryset = CompanyMpoTourPlan.objects.select_related(
        "mpo_name__company_name",
        "mpo_name__user_name",
        "mpo_name__role_name",
        "mpo_name__executive_level",
        "mpo_name__role_name__role_name",
        "mpo_name",
        "company_name",
        "tour_plan",
        "tour_plan__shift",
        "tour_plan__tour_plan",
        "approved_by",
        "approved_by__company_name",
        "approved_by__user_name",
        "approved_by__role_name",
        "approved_by__executive_level",
        "approved_by__role_name__role_name",
    )
    serializer_class = CompanyMpoTourPlanSerializer
    filter_backends = [CaseInsensitiveDjangoFilterBackend]
    filter_fields = [
        "id",
        "mpo_name_id",
        "tour_plan__tour_plan__select_the_month",
        "tour_plan__tour_plan__select_the_date_id",
        "tour_plan__tour_plan__is_dcr_added",
        "tour_plan__tour_plan__year",
        "is_missed_call_calculated",
        "is_approved",
        "company_name",
        "mpo_name__role_name__role_name",
    ]
    case_insensitive_fields = ["tour_plan__tour_plan__select_the_month", "is_approved"]


class CompanyMpoTourplanViewset(viewsets.ModelViewSet):
    model = CompanyMpoTourPlan
    queryset = CompanyMpoTourPlan.objects.select_related(
        "mpo_name__company_name",
        "mpo_name__user_name",
        "mpo_name__role_name",
        "mpo_name__executive_level",
        "mpo_name__role_name__role_name",
        "mpo_name",
        "company_name",
        "tour_plan",
        "tour_plan__shift",
        "tour_plan__tour_plan",
        "approved_by",
        "approved_by__company_name",
        "approved_by__user_name",
        "approved_by__role_name",
        "approved_by__executive_level",
        "approved_by__role_name__role_name",
    )
    serializer_class = CompanyMpoTourPlanSerializer
    pagination_class = CustomPagination
    # permission_classes = [IsAuthenticated]
    # filter_backends = [CaseInsensitiveDjangoFilterBackend]
    filter_backends = [DjangoFilterBackend]
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "id",
        "mpo_name_id",
        "tour_plan__tour_plan__select_the_month",
        "tour_plan__tour_plan__select_the_date_id",
        "tour_plan__tour_plan__is_dcr_added",
        "tour_plan__tour_plan__year",
        "is_approved",
        "company_name",
        "tour_plan__tour_plan__is_admin_opened",
        "mpo_name__role_name__role_name",
        "tour_plan__shift_id",
        "is_missed_call_calculated",
    ]
    case_insensitive_fields = ["tour_plan__tour_plan__select_the_month", "is_approved"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(mpo_name__user_name__is_active=False).order_by(
            "tour_plan__tour_plan__select_the_date_id"
        )

    @action(detail=False, methods=["GET"])
    def get_tour_plan_mpo(self, request):
        company_user_role = CompanyUserRole.objects.get(id=request.GET.get("mpo_name"))
        if company_user_role.is_tp_locked:
            return Response(
                data={"status": "Your user has been locked"}, status=status.HTTP_200_OK
            )

        if self.is_locked_tour_plan_mpo(request):
            company_user_role.is_tp_locked = True
            company_user_role.save()
            self.is_locked_tour_plan_mpo(is_locked=True)

            return Response(
                data={"status": "Your user has been locked"}, status=status.HTTP_200_OK
            )

        tour_plan_list = CompanyMpoTourPlan.objects.filter(
            (
                Q(
                    tour_plan__tour_plan__select_the_date_id__in=[
                        date(nepali_today.year, nepali_today.month, nepali_today.day),
                        date(
                            nepali_today.year, nepali_today.month, nepali_today.day - 1
                        ),
                        date(
                            nepali_today.year, nepali_today.month, nepali_today.day - 2
                        ),
                    ]
                )
                | Q(tour_plan__tour_plan__is_admin_opened=True)
            ),
            mpo_name=request.GET.get("mpo_name"),
            is_approved=True,
            is_locked=False,
        )
        serializer = CompanyMpoTourPlanSerializer(
            tour_plan_list, many=True, context={"request": request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def is_locked_tour_plan_mpo(self, request, is_locked=False):
        company_lock_day = CompanyRolesTPLock.objects.get(
            company_roles=CompanyUserRole.objects.get(
                id=request.GET.get("mpo_name")
            ).role_name
        ).tp_lock_days
        latest_date_list = [
            date(nepali_today.year, nepali_today.month, nepali_today.day - day)
            for day in range(1, company_lock_day + 1)
        ]
        tour_plan_list = CompanyMpoTourPlan.objects.filter(
            ~Q(tour_plan__tour_plan__select_the_date_id__in=latest_date_list),
            (
                Q(tour_plan__tour_plan__is_dcr_added=False)
                | Q(tour_plan__tour_plan__is_doctor_dcr_added=False)
                | Q(tour_plan__tour_plan__is_chemist_dcr_added=False)
                | Q(tour_plan__tour_plan__is_stockist_dcr_added=False)
            ),
            mpo_name=request.GET.get("mpo_name"),
            is_approved=True,
            tour_plan__tour_plan__is_admin_opened=False,
            tour_plan__tour_plan__select_the_date_id__lte=date(
                nepali_today.year, nepali_today.month, nepali_today.day
            ),
        )
        if is_locked:
            tour_plan_list.update(is_locked=True)
            return {}
        return len(tour_plan_list) == company_lock_day

    def create(self, request, *args, **kwargs):
        # data = mpo_data_transmission(request)
        serializer = CompanyMpoTourPlanSerializer(
            data=request.data, many=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            # if get_upper_level_user_id(data[0]['mpo_name']) and get_user_id(data[0]['mpo_name']):
            #     general_notification_send(
            #         {
            #             'type':"Tourplan",
            #             "receiver_id":get_upper_level_user_id(data[0]['mpo_name']),
            #             "sender_name":get_user_name(data[0]['mpo_name']),
            #             "url":"",
            #             "sender_id":get_user_id(data[0]['mpo_name']),
            #             "notification_title":"Tourplan Created",
            #             "notification_description":f"{get_user_name(data[0]['mpo_name'])} has succesfully created Tourplan"
            #         }
            #     )
            return Response(
                data=serializer.data, status=status.HTTP_200_OK
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        update_instance = CompanyMpoTourPlan.objects.get(id=id)
        data = mpo_update_data_transmission(request)
        serializer = self.serializer_class(
            update_instance, data=data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            # if get_upper_level_user_id(update_instance.mpo_name.id) and get_user_id(update_instance.mpo_name.id):
            #     general_notification_send(
            #     {
            #         'type':"Tourplan",
            #         "receiver_id":get_upper_level_user_id(update_instance.mpo_name.id),
            #         "sender_name":get_user_name(update_instance.mpo_name.id),
            #         "url":"",
            #         "sender_id":get_user_id(update_instance.mpo_name.id),
            #         "notification_title":"Tourplan Updated",
            #         "notification_description":f"{get_user_name(update_instance.mpo_name.id)} has updated Tourplan"
            #     }
            # )
            return Response(serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def destroy_tour_plan_with_shift_and_mpo(self, request, *args, **kwargs):
        mpo_shiftwise_tour_plan_id = kwargs.get("pk")
        mpo_shiftwise_tour_plan_instance = CompanyMpoTourPlan.objects.get(
            id=mpo_shiftwise_tour_plan_id
        )
        shift_wise_tour_plan_id = mpo_shiftwise_tour_plan_instance.tour_plan.id
        shift_wise_tour_plan_instance = ShiftWiseTourplan.objects.get(
            id=shift_wise_tour_plan_id
        )
        tour_plan_id = shift_wise_tour_plan_instance.tour_plan.id
        tour_plan_instance = TourPlan.objects.get(id=tour_plan_id)
        tour_plan_instance.delete()
        return Response("data deleted successfully")

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def get_missed_calls(self, request):
        month = request.data.get("month")
        company_id = request.data.get("company")
        role_id = request.data.get("role")
        company_user_list = [
            (i.id, i.user_name)
            for i in CompanyUserRole.objects.filter(
                company_name=company_id, role_name=role_id
            )
        ]
        missed_call_data = {}
        for i in company_user_list:
            missed_call_data[i[1].email] = CompanyMpoTourPlan.objects.filter(
                tour_plan__tour_plan__select_the_month=month,
                tour_plan__tour_plan__is_dcr_added=False,
            ).count()
        return Response(data=missed_call_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def get_missed_tourplans(self, request):
        today = date.today()
        tour_plans_before_today = CompanyMpoTourPlan.objects.filter(
            mpo_name=request.data.get("mpo_id"),
            tour_plan__tour_plan__select_the_date_id__lt=today,
            tour_plan__tour_plan__is_dcr_added=False,
            is_approved=True,
        )
        serializer = self.serializer_class(tour_plans_before_today, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
@permission_classes((AllowAny,))
def bulk_create_mpo_tour_plan(request):
    for i in request.data:
        tour_plan_instance = TourPlan(
            select_the_month=get_year_month_from_date(i["dates"]),
            select_the_date_id=i["dates"],
            select_the_area=i["select_the_area"],
            purpose_of_visit=i["purpose_of_visit"],
            is_unplanned=False,
        )
        tour_plan_instance.save()
        shift_instance = Shift.objects.get(id=i["shift"])
        shift_wise_tour_plan_instance = ShiftWiseTourplan(
            tour_plan=tour_plan_instance, shift=shift_instance
        )
        shift_wise_tour_plan_instance.save()

        company_mpo_tour_plan = CompanyMpoTourPlan(
            mpo_name=i["mpo_name"],
            tour_plan=shift_wise_tour_plan_instance,
            # submit_to = validated_data.get('submit_to'),
            company_name=i["company_name"],
        )
        company_mpo_tour_plan.save()


@api_view(["POST"])
@permission_classes((AllowAny,))
def tour_plan_same_as_previous_month(request):
    previous_month_tour_plan = CompanyMpoTourPlan.objects.filter(
        tour_plan__tour_plan__select_the_month=request.data.get("month"),
        tour_plan__tour_plan__select_the_date_id__year=request.data.get("year"),
        mpo_name=request.data.get("mpo_name"),
    )
    if not previous_month_tour_plan.exists():
        return Response(
            data="No previous data present!!!!", status=status.HTTP_400_BAD_REQUEST
        )
    for i in previous_month_tour_plan:
        this_month_tour_plan = TourPlan.objects.filter(
            select_the_date_id=i.tour_plan.tour_plan.select_the_date_id
        ).exists()
        if not this_month_tour_plan:
            tour_plan = TourPlan(
                select_the_month=get_next_month(request.data.get("month")),
                select_the_date_id=get_next_month_date(
                    i.tour_plan.tour_plan.select_the_date_id
                ),
                select_the_area=i.tour_plan.tour_plan.select_the_area,
                purpose_of_visit=i.tour_plan.tour_plan.purpose_of_visit,
                is_dcr_added=i.tour_plan.tour_plan.is_dcr_added,
                is_unplanned=i.tour_plan.tour_plan.is_unplanned,
            )
            tour_plan.save()

            shift_wise_tour_plan_instance = ShiftWiseTourplan(
                tour_plan=tour_plan, shift=i.tour_plan.shift
            )
            shift_wise_tour_plan_instance.save()

            company_mpo_tour_plan = CompanyMpoTourPlan(
                mpo_name=i.mpo_name,
                tour_plan=shift_wise_tour_plan_instance,
                # submit_to = validated_data.get('submit_to'),
                company_name=i.company_name,
                is_approved=False,
            )
            company_mpo_tour_plan.save()

    return Response(
        data="Successfully created tour plan for new month!!!!",
        status=status.HTTP_200_OK,
    )


@api_view(["post"])
@permission_classes((IsAuthenticated,))
def tour_plan_bulk_update_by_month(request):
    if (
        request.data.get("month")
        and request.data.get("year")
        and request.data.get("mpo_name")
    ):
        instance = CompanyMpoTourPlan.objects.filter(
            tour_plan__tour_plan__select_the_month=request.data.get("month"),
            tour_plan__tour_plan__select_the_date_id__year=request.data.get("year"),
            mpo_name=request.data.get("mpo_name"),
        ).update(is_approved=True, approved_by=request.data.get("approved_by"))
        return Response("updated successfully")
    else:
        return Response(
            data={"data": "Please send all the fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def get_the_mpo_tourplan_of_30_days(request):
    current_date = datetime.now()
    new_date = current_date + timedelta(days=30)
    new_date_string = new_date.strftime("%Y-%m-%d")
    company_mpo_tour_plan_list = CompanyMpoTourPlan.objects.filter(
        Q(mpo_name__id=request.data.get("id"))
        & Q(
            tour_plan__tour_plan__select_the_date_id__range=(
                current_date.strftime("%Y-%m-%d"),
                new_date_string,
            )
        )
    )
    serializer = CompanyMpoTourPlanSerializer(
        company_mpo_tour_plan_list, many=True, context={"request": request}
    )
    return JsonResponse(
        serializer.data,
        status=200,
        headers={"content_type": "application/json"},
        safe=False,
    )


@api_view(["POST"])
@permission_classes((AllowAny,))
def get_mpo_list(request):
    mpo_list = CompanyUserRole.objects.filter(
        company_name=request.data.get("company_name"),
        role_name__role_name__role_name__in=["mpo", "MPO", "Mpo"],
        user_name__is_active=True,
    )
    serializers = CompanyUserRoleSerializers(mpo_list, many=True)
    return Response(data=serializers.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((AllowAny,))
def transfer_mpo_chemist_doctor(request):
    transfer_to_mpo = request.data.get("transfer_to_mpo")
    transfer_from_mpo = request.data.get("transfer_from_mpo")
    area = request.data.get("area")
    company_area = CompanyMPOArea.objects.get(id=area)
    company_area_instance = CompanyMPOArea(
        company_name=company_area.company_name,
        mpo_name=CompanyUserRole.objects.get(id=transfer_to_mpo),
        latitude=company_area.latitude,
        longitude=company_area.longitude,
        country=company_area.country,
        state=company_area.state,
        division=company_area.division,
        area_name=company_area.area_name,
        station_type=company_area.station_type,
        company_area=company_area.company_area,
    )
    if not CompanyMPOArea.objects.filter(
        mpo_name__id=transfer_to_mpo, company_area=company_area.company_area
    ).exists():
        company_area_instance.save()
    doctor_from_mpo = CompanyWiseDoctor.objects.filter(
        mpo_name=transfer_from_mpo, doctor_name__doctor_territory=area
    )

    if (
        doctor_from_mpo.exists()
        and not CompanyWiseDoctor.objects.filter(
            mpo_name__id=transfer_to_mpo, doctor_name=doctor_from_mpo[0].doctor_name
        ).exists()
    ):
        doctors_list = [
            CompanyWiseDoctor(
                company_name=doctor.company_name,
                doctor_name=doctor.doctor_name,
                mpo_name=CompanyUserRole.objects.get(id=transfer_to_mpo),
                is_investment=doctor.is_investment,
            )
            for doctor in doctor_from_mpo
        ]
        CompanyWiseDoctor.objects.bulk_create(doctors_list)
    chemist_from_mpo = CompanyWiseChemist.objects.filter(
        mpo_name=transfer_from_mpo, chemist_name__chemist_territory=area
    )
    if (
        chemist_from_mpo.exists()
        and not CompanyWiseChemist.objects.filter(
            mpo_name__id=transfer_to_mpo, chemist_name=chemist_from_mpo[0].chemist_name
        ).exists()
    ):
        chemist_list = [
            CompanyWiseChemist(
                company_name=chemist.company_name,
                chemist_name=chemist.chemist_name,
                mpo_name=CompanyUserRole.objects.get(id=transfer_to_mpo),
                is_investment=chemist.is_investment,
            )
            for chemist in chemist_from_mpo
        ]
        CompanyWiseChemist.objects.bulk_create(chemist_list)
    return Response(
        data={"msg": "Successfully transferred the data."}, status=status.HTTP_200_OK
    )


# TODO place this in cron job
# @api_view(['GET'])
# def get_missed_call_data(request):
