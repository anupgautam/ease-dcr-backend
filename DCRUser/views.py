from itertools import chain
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action, permission_classes
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q
from django.http import JsonResponse
import jwt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from Company.models import Company
from DCRUser.logic import generate_random_password
from DCR.settings import SECRET_KEY
from DCRUser.models import (
    User,
    CompanyUser,
    CompanyUserRole,
)
from DCRUser.serializers import *
from Account.serializers import UserCreationSerializer
from Account.pagination import CustomPagination
from Company.models import *
from DCRUser.logic import get_user_from_access
from DCRUser.utils import company_user_data_transmission


class UserViewset(viewsets.ModelViewSet):
    queryset = CompanyUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("data added")
        else:
            return Response(serializer.errors)

    def get_serializer_class(self):
        if self.action == "create":
            return AddCompanyUserSerializers
        else:
            return UserSerializers


class CompanyUserViewset(viewsets.ModelViewSet):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyUserSerializers
    pagination_class = CustomPagination
    filterset_fields = ["company_name", "user_name__is_active"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("user_name__first_name")
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(role_name__role_name__role_name="admin")


class CompanyUserWithoutPagination(viewsets.ModelViewSet):
    queryset = CompanyUser.objects.all()
    serializer_class = CompanyUserSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["company_name", "user_name__is_active"]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("user_name__first_name")
    


class CompanyUserRoleViewsetWithoutPagination(viewsets.ModelViewSet):
    queryset = CompanyUserRole.objects.all()
    serializer_class = CompanyUserRoleSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "company_name",
        "executive_level",
        "role_name",
        "role_name__role_name__role_name",
        "user_name__is_active",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("user_name__first_name")
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(role_name__role_name__role_name="admin")


class CompanyUserRoleViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = CompanyUserRole.objects.all()
    serializer_class = CompanyUserRoleSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "id",
        "role_name",
        "role_name__role_name",
        "company_name__company_id",
        "user_name",
        "user_name__is_active",
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("user_name__first_name")

    @action(detail=False, methods=["post"])
    @permission_classes(
        [
            IsAuthenticated,
        ]
    )
    def create_role_user_and_company_user_role(self, request, *args, **kwargs):
        email = request.data.get("email")
        company_user_role_data = company_user_data_transmission(
            email=email, request=request
        )
        serializer = self.serializer_class(data=company_user_role_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"])
    @permission_classes(
        [
            IsAuthenticated,
        ]
    )
    def update_data(self, request, *args, **kwargs):
        email = request.data.get("email")
        if User.objects.filter(email=email).count() > 0:
            email = "xyz@gmail.com"
        company_user_id = kwargs.get("pk")
        company_user_instance = CompanyUserRole.objects.get(id=company_user_id)
        update_data = company_user_data_transmission(email=email, request=request)
        update_serializer = CompanyUserRoleSerializers(
            company_user_instance, data=update_data, partial=True
        )
        if update_serializer.is_valid():
            update_serializer.save()
            return Response({"data": update_serializer.data})
        else:
            return Response({"error": update_serializer.errors})

    @action(detail=False, methods=["post"])
    def search_user(self, request):
        query = request.data.get("search")
        result = (
            CompanyUserRole.objects.annotate(
                similarity=Greatest(
                    TrigramSimilarity("company_name__company_name", query),
                    TrigramSimilarity("user_name__first_name", query),
                    TrigramSimilarity("role_name__role_name__role_name", query),
                )
            ).filter(
                Q(company_name__company_name__trigram_similar=query)
                | Q(user_name__first_name__trigram_similar=query)
                | Q(role_name__role_name__role_name=query),
                similarity__gt=0.1,
            )
        ).order_by("-similarity")

        serializer = self.get_serializer(result, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        company_user_role_instance = CompanyUserRole.objects.get(id=kwargs.get("pk"))
        user_instance = User.objects.get(id=company_user_role_instance.user_name.id)
        user_instance.delete()
        # user_instance.save()
        return Response("data deleted successfully")
        # return super().destroy(request, *args, **kwargs)


class CompanyUserAttendanceViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = CompanyUserAttendance.objects.all()
    serializer_class = CompanyUserAttendanceSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "id",
        "company_name",
        "user_id",
        "month",
        "attendance_date",
        "is_leave",
        "leave_type",
    ]

@api_view(["POST"])
def make_user_present(request):
    company_instance = Company.objects.get(
        company_id=request.data.get('company_name')
    )
    user_instance = CompanyUserRole.objects.get(
        id=request.data.get('user_id')
    )
    attendance_date = request.data.get('attendance_date')
    month = request.data.get('month')
    attendance_instance = CompanyUserAttendance(
        company_name=company_instance,
        user_id=user_instance,
        attendance_date=attendance_date,
        month=month
    )
    attendance_instance.save()
    return JsonResponse(
            {"success":"User marked present"}, status=200, headers={"content_type": "application/json"}, safe=False
        )




# This api view returns the upper level company users according the role id
@api_view(["POST"])
def get_upper_company_user_from_company_name_and_role_name(request):
    company_role_instance = CompanyRoles.objects.get(id=request.data.get("role_id"))
    if CompanyRoles.objects.filter(
        priority_value=company_role_instance.priority_value + 1
    ).exists():
        upper_level = CompanyRoles.objects.get(
            priority_value=company_role_instance.priority_value + 1,
            company_name=company_role_instance.company_name,
        )
        company_user_role_ids = CompanyUserRole.objects.filter(role_name=upper_level)
        company_users = []
        for i in company_user_role_ids:
            instance = CompanyUser.objects.get(user_name=i.user_name.id)
            company_users.append(instance)
        serializer = CompanyUserSerializers(company_users, many=True)
        return JsonResponse(
            serializer.data,
            status=200,
            headers={"content_type": "application/json"},
            safe=False,
        )
    else:
        return JsonResponse(
            [], status=200, headers={"content_type": "application/json"}, safe=False
        )


# This api view returns one level up upper executives(company user role)
@api_view(["POST"])
def get_executives_from_user_id(request):
    company_user_role_instance = CompanyUserRole.objects.get(
        id=request.data.get("user_id")
    )
    if CompanyRoles.objects.filter(
        priority_value=company_user_role_instance.role_name.priority_value + 1
    ).exists():
        company_role_instance = CompanyRoles.objects.get(
            priority_value=company_user_role_instance.role_name.priority_value + 1,
            company_name__company_id=company_user_role_instance.company_name.company_id,
        )
        if CompanyUserRole.objects.filter(role_name=company_role_instance.id).exists():
            user_list = CompanyUserRole.objects.filter(
                role_name=company_role_instance.id
            )
            serializer = CompanyUserRoleSerializers(user_list, many=True)
            return JsonResponse(
                serializer.data,
                status=200,
                headers={"content_type": "application/json"},
                safe=False,
            )
        else:
            return JsonResponse(
                [], status=200, headers={"content_type": "application/json"}, safe=False
            )
    else:
        return JsonResponse(
            [], status=200, headers={"content_type": "application/json"}, safe=False
        )


# this api view returns all the upper level executives(company user role)
# @api_view(['POST'])
# def get_all_the_upper_level_users_from_company_user_role_id(request):
#     user_list = []
#     user_id = request.data.get('id')
#     if(request.data.get('id')):
#         while True:
#             if CompanyUserRole.objects.filter(id=user_id).exists():
#                 company_user_role_instance = CompanyUserRole.objects.get(id=user_id)
#                 if company_user_role_instance.executive_level != None:
#                     company_user_instance1 = CompanyUser.objects.get(id=company_user_role_instance.executive_level.id)
#                     user_instance1 = User.objects.get(id=company_user_instance1.user_name.id)
#                     if CompanyUserRole.objects.filter(user_name=user_instance1.id).exists():
#                         company_user_role_instance2 = CompanyUserRole.objects.get(user_name=user_instance1.id)
#                         user_list.append(company_user_role_instance2)
#                         user_id = company_user_role_instance2.id
#                     else:
#                         break
#                 else:
#                     break
#             else:
#                 break
#     serializer = CompanyUserRoleSerializers(user_list, many=True)
#     return JsonResponse(serializer.data,status=200,headers={'content_type':'application/json'}, safe=False)


def get_lower_level_instances(company_user_instance, instance_dict):
    if len(company_user_instance) == 0:
        return instance_dict
    if company_user_instance[0].role_name.priority_value == 0:
        instance_dict["mpo"] = [company_user_instance]
        return instance_dict
    else:
        if instance_dict.get("other_roles"):
            instance_dict["other_roles"].append(company_user_instance)
        else:
            instance_dict["other_roles"] = [company_user_instance]
        company_user_list = CompanyUser.objects.filter(
            user_name__id__in=[
                instance.user_name.id for instance in company_user_instance
            ]
        )
        lower_level_instance = CompanyUserRole.objects.filter(
            executive_level__in=company_user_list
        )
        return get_lower_level_instances(lower_level_instance, instance_dict)


# This api view returns all the lower executives(company user role) from company user role id
@api_view(["POST"])
def get_all_the_lower_level_users_from_company_user_role_id(request):
    user_dict = {}
    user_id = request.data.get("id")
    data = []
    if request.data.get("id"):
        if CompanyUserRole.objects.filter(id=user_id).exists():
            company_user_role_instance = CompanyUserRole.objects.get(id=user_id)
            company_user_instance = CompanyUser.objects.get(
                user_name=company_user_role_instance.user_name.id
            )
            if CompanyUserRole.objects.filter(
                executive_level=company_user_instance.id
            ).exists():
                lower_level_instances = CompanyUserRole.objects.filter(
                    executive_level=company_user_instance.id
                )
                data = get_lower_level_instances(lower_level_instances, user_dict)

    if len(data) == 0:
        return JsonResponse(
            data, status=200, headers={"content_type": "application/json"}, safe=False
        )
    user_list = list(chain.from_iterable(data.values()))
    if len(user_list) == 2:
        queryset = list(chain(user_list[0], user_list[1]))
    else:
        queryset = user_list[0]
    serializer = CompanyUserRoleSerializers(queryset, many=True)
    return JsonResponse(
        serializer.data,
        status=200,
        headers={"content_type": "application/json"},
        safe=False,
    )


def get_higher_level_instances(user_id, data):
    if CompanyUserRole.objects.filter(id=user_id).exists():
        higher_order_company_user = CompanyUserRole.objects.get(
            id=user_id
        ).executive_level
        if not higher_order_company_user or higher_order_company_user == "null":
            return data
        else:
            company_user_role = CompanyUserRole.objects.get(
                user_name=higher_order_company_user.user_name
            )
            data.append(company_user_role)
            return get_higher_level_instances(company_user_role.id, data)


@api_view(["POST"])
def get_all_the_upper_level_users_from_company_user_role_id(request):
    print("hamro request")
    print("id ho hai",request.data.get('id'))
    user_dict = {}
    user_id = request.data.get("id")
    data = []
    if request.data.get("id"):
        data = get_higher_level_instances(user_id, data)
        print(data)
    else:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"data": "Sorry! No such user present"},
        )
    if len(data) == 0:
        return JsonResponse(
            data, status=200, headers={"content_type": "application/json"}, safe=False
        )
    serializer = CompanyUserRoleSerializers(data, many=True)
    print("hamro data")
    print(serializer.data)
    return JsonResponse(
        serializer.data,
        status=200,
        headers={"content_type": "application/json"},
        safe=False,
    )


@api_view(["POST"])
def get_admin_user_id(request):
    if request.data.get("company_id"):
        if CompanyUserRole.objects.filter(
            company_name__company_id=request.data.get("company_id"),
            role_name__role_name__role_name="admin",
        ).exists():
            company_user_role_instance = CompanyUserRole.objects.get(
                company_name__company_id=request.data.get("company_id"),
                role_name__role_name__role_name="admin",
            )
            return Response(
                company_user_role_instance.user_name.id,
                status=200,
                headers={"content_type": "application/json"},
            )
        else:
            return Response("Admin User doesnot exists")


@api_view(["POST"])
def get_user_hierarchy(request):
    sending_data = []
    company_user_role_instance = CompanyUserRole.objects.filter(
        company_name__company_id=request.data.get("company_id")
    )
    country_head_instance = CompanyUserRole.objects.get(
        company_name__company_id=request.data.get("company_id"),
        role_name__role_name__role_name="ch",
    )
    company_user_instance = CompanyUser.objects.get(
        user_name=country_head_instance.user_name
    )
    for i in company_user_role_instance:
        if i.executive_level:
            if i.executive_level.id == company_user_instance.id:
                pass
