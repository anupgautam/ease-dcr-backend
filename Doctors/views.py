from calendar import c
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_multiple_model.views import ObjectMultipleModelAPIView
from django_filters.rest_framework import DjangoFilterBackend
from Doctors.apps import DoctorsConfig
# from query_counter.decorators import queries_counter
from django.conf import settings
from django.db import connection
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


from Doctors.models import *
from Doctors.serializers import *
from Account.pagination import CustomPagination
from Doctors.utils import (doctor_data_transmission,
                           doctor_category_data)
from Doctors.search import TrigramSearch
from Doctors.description import Search
from Doctors.search import CompanyWiseTrigramSearch


class DoctorViewset(viewsets.ModelViewSet):
    serializer_class = DoctorSerializers
    queryset = Doctor.objects.all()
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('doctor_name')

    def create(self, request, *args, **kwargs):
        doctor_data = doctor_data_transmission(request)
        if not request.data.get('doctor_territory'):
            return Response(
                data={"Doctor Territory cant be null"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.data.get('doctor_specialization'):
            return Response(
                data={"Doctor Specialization cant be null"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer_class()(data=doctor_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data={"Data saved successfully"},
                status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
                        
    def get_serializer_class(self):
        if self.action == "create":
            return AddDoctorSerializer
        else:
            return DoctorSerializers

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        doctor_instance = Doctor.objects.get(id=id)
        data = doctor_data_transmission(request)
        serializer = AddDoctorSerializer(doctor_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DoctorCategoryViewset(viewsets.ModelViewSet):
    model = DoctorCategory
    queryset = DoctorCategory.objects.all()
    serializer_class = DoctorCategorySerializers


class CompanyDoctorSpecializationViewset(viewsets.ModelViewSet):
    model = CompanyDoctorSpecialization
    queryset = CompanyDoctorSpecialization.objects.all()
    serializer_class = CompanyDoctorSpecializationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name']

    # def create(self, request, *args, **kwargs):
    #     data = doctor_category_data(request)
    #     serializer = self.serializer_class(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def destroy(self, request, *args, **kwargs):
    #     instance = CompanyDoctorCategory.objects.get(
    #     id=kwargs.get('pk'))
    #     category_instance = DoctorCategory.objects.get(
    #     id=instance.category_name.id)
    #     category_instance.delete()
    #     instance.delete()
    #     return Response({'success':'data deleted successfully'})
    # def update(self, request, *args, **kwargs):
    #     data = doctor_data_transmission(request)
    #     instance = CompanyDoctorCategory.objects.get(id=kwargs.get('pk'))
    #     serializer = self.serializer_class(instance, data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)

# class CompanyWiseDoctorViewset(viewsets.ModelViewSet):
#     model = CompanyWiseDoctor
#     queryset = CompanyWiseDoctor.objects.all()
#     serializer_class = CompanyWiseDoctorSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['id', 'company_name']


# class CategoryWiseDoctorViewset(viewsets.ModelViewSet):
#     model = CategoryWiseDoctor
#     pagination_class = CustomPagination
#     queryset = CategoryWiseDoctor.objects.all()
#     serializer_class = CategoryWiseDoctorSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['doctor_name']

class CompanyWiseDoctorWithOutPagination(viewsets.ModelViewSet):
    model = CompanyWiseDoctor
    queryset = CompanyWiseDoctor.objects.all()
    serializer_class = CompanyWiseDoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name', 'doctor_name__doctor_territory', 'mpo_name']

class CompanyWiseDoctorViewset(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    model = CompanyWiseDoctor
    queryset = CompanyWiseDoctor.objects.all()
    serializer_class = CompanyWiseDoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name', 'doctor_name__doctor_territory', 'mpo_name']
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('doctor_name__doctor_name').exclude(mpo_name__user_name__is_active=False)

    @action(detail=False, methods=['post'])
    def search_doctor(self, request, *args, **kwargs):
        search_data = CompanyWiseTrigramSearch(request.data.get('search'),
                             'CompanyWiseDoctor',
                             ['doctor_name__doctor_name',
                              'doctor_name__doctor_address',
                              'doctor_name__doctor_phone_number'],
                              'Doctors',
                              request.data.get('company_id')
                              )
        serializer = self.get_serializer(search_data.search(), many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([])
        
    # def create(self, request, *args, **kwargs):
    #     doctor_name = DoctorSerializers(data=request.data)
    #     if doctor_name.is_valid():
    #         doctor_name.save()
    #     else:
    #         return Response(data=doctor_name.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializers = self.get_serializer(
    #         {
    #             'company_name': request.data.get('company_name'),
    #             'doctor_name': doctor_name.id,
    #             'mpo_name': request.data.get('mpo_name')
    #             })
    #     if serializers.is_valid():
    #         serializers.save()
    #         return Response(data=serializers.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        

class DoctorEventsViewset(viewsets.ModelViewSet):
    model = DoctorEvents
    queryset = DoctorEvents.objects.all()
    serializer_class = DoctorEventSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'mpo_id','doctor_id__company_name']

    # def create(self, request, *args, **kwargs):
    #     if not request.data.get('event_type') or request.data.get('event_type') == '':
    #         return Response(
    #             data={'Event type cant be null'},
    #             status=status.HTTP_400_BAD_REQUEST)
    #     if not request.data.get('event_date'):
    #         return Response(
    #             data={'Event date cannot be null.'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return super().create(request, *args, **kwargs)
    
    # def update(self, request, *args, **kwargs):
    #     if not request.data.get('event_type') or request.data.get('event_type') == '':
    #         return Response(
    #             data={'Event type cant be null'},
    #             status=status.HTTP_400_BAD_REQUEST)
    #     if not request.data.get('event_date'):
    #         return Response(
    #             data={'Event date cannot be null.'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return super().update(request, *args, **kwargs)
    
    # def partial_update(self, request, *args, **kwargs):
    #     if not request.data.get('event_type') or request.data.get('event_type') == '':
    #         return Response(
    #             data={'Event type cant be null'},
    #             status=status.HTTP_400_BAD_REQUEST)
    #     if not request.data.get('event_date'):
    #         return Response(
    #             data={'Event date cannot be null.'},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     return super().partial_update(request, *args, **kwargs)
    

class DoctorEventsViewsetWithOutPagination(viewsets.ModelViewSet):
    model = DoctorEvents
    queryset = DoctorEvents.objects.all()
    serializer_class = DoctorEventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'mpo_id']

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
 