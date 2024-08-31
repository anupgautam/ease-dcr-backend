from argparse import Action
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from rest_framework.permissions import *
# from rest_framework.authentication import *
from rest_framework.decorators import action
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from Stockist.serializers import *
from Stockist.models import *
from Account.pagination import CustomPagination
from DCRUser.logic import get_user_from_access
from Stockist.utils import stockist_data_transmission
from Doctors.search import TrigramSearch
from Doctors.description import Search
from Doctors.search import CompanyWiseTrigramSearch


class StockistViewset(viewsets.ModelViewSet):
    queryset = Stockist.objects.all()
    pagination_class = CustomPagination
    serializer_class = StockistSerializers
    filterset_fields = ['id','stockist_territory']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('stockist_name')
    
    # def create(self, request, *args, **kwargs):
    #     
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         serializer.is_valid()
    #         serializer.save()
    #     except Exception as e:
    #         
    #         
    #     return Response({'data':serializer.data},
    #                         status=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     
    #     return Response({"data":"success"})
    #     # return super().list(request, *args, **kwargs)

    # def get_serializer_class(self):
    #     
    #     if self.action == "create":
    #         return StockistAddSerializer
    #     else:
    #         return StockistSerializers
    #     return StockistSerializers 


class CompanyStockistWithoutPaginationViewset(viewsets.ModelViewSet):
    model = CompanyStockist
    queryset = CompanyStockist.objects.all()
    serializer_class = CompanyStockistSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name','stockist_name__stockist_territory']


class CompanyStockistViewset(viewsets.ModelViewSet):
    model = CompanyStockist
    queryset = CompanyStockist.objects.all()
    serializer_class = CompanyStockistSerializers
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name','stockist_name__stockist_territory']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('stockist_name__stockist_name').exclude(mpo_name__user_name__is_active=False)

    @action(detail=False, methods=['post'])
    def create_stockist(self, request, *args, **kwargs):
        data = stockist_data_transmission(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['put'])
    def update_stockist(self, request, *args, **kwargs):
        stockist_id = kwargs.get('pk')
        update_data = stockist_data_transmission(request)
        stockist_instance = CompanyStockist.objects.get(id=stockist_id)
        serializer = self.serializer_class(stockist_instance,
                                            data=update_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

            
    @action(detail=False, methods=['post'])
    def search_stockist(self, request, *args, **kwargs):
        search_data = CompanyWiseTrigramSearch(request.data.get('search'),
                             'CompanyStockist',
                             ['stockist_name__stockist_name',
                              'stockist_name__stockist_address',
                              'stockist_name__stockist_contact_number'],
                              'Stockist',
                              request.data.get('company_id')
                              )
        serializer = self.get_serializer(search_data.search(), many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([])
        

class CompanyMPOStockistViewSet(viewsets.ModelViewSet):
    model = CompanyMPOStockist
    queryset = CompanyMPOStockist.objects.all()
    serializer_class = CompanyMPOStockistSerializers
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'mpo_name',
        'stockist_name__stockist_name__stockist_territory']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        if serializer.is_valid():
            # Perform the bulk create operation
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def perform_bulk_create(self, serializer):
        serializer.save()
        

    

    
