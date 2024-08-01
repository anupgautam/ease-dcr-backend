from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from dailycallrecord.models import (MpoWiseShiftwiseDcrForChemist,
                                    DcrForChemistProduct,
                                    ChemistOrderedProductInformationMap,
                                    ChemistOrderedProductInformation,
                                    DcrForStockistOrderedProduct,
                                    MpoWiseShiftwiseDcrForStockist,
                                    StockistOrderedProduct
                                     )
from Chemist.models import CompanyWiseChemist
from Stockist.models import CompanyStockist
from Account.pagination import paginate_json_response

from Product.serializers import *
from Account.pagination import CustomPagination
from Product.utils import product_data_transmission
from Doctors.search import TrigramSearch
from Doctors.description import Search
from Doctors.search import CompanyWiseTrigramSearch


class ProductViewset(viewsets.ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('product_name')
    
    # def create(self, request, *args, **kwargs):
    #     
    #     serializer = self.get_serializer(data=request.data)
    #     try:
    #         serializer.is_valid()
    #         serializer.save()
    #     except Exception as e:
    #         
    #         
    #     return Response({'data':"error occured"},
    #                         status=status.HTTP_201_CREATED)

    # def get_serializer_class(self):
    #     if self.action == "create":
    #         return ProductAddSerializers
    #     else:
    #         return ProductSerializer
    #     return ProductSerializer


# class ProductViewset(viewsets.ModelViewSet):
    # pagination_class = CustomPagination
    # queryset = Product.objects.all()
    # serializer_class = ProductAddSerializers

    # @action(detail=False, methods=['post'])
    # def create_product(self, request, *args, **kwargs):
    #     company_name = get_user_from_access(request.data.get('access'))
    #     product_data = {
    #         'product_name': request.data.get('product_name'),
    #         'product_molecular_name': request.data.get('product_molecular_name'),
    #         'product_price_per_strip_in_mrp': request.data.get('product_price_per_strip_in_mrp'),
    #         'product_price_for_stockiest': request.data.get('product_price_for_stockiest'),
    #     }
    #     product_serializer = ProductAddSerializers(data=product_data)
    #     company_product_data = {
    #         'company_name': company_name,
    #         'product_name': product_data.get('id')
    #     }
    #     product_serializer = self.serializer_class(
    #         data=product_data
    #     )
    #     if product_serializer.is_valid():
    #         product_serializer.save()
    #         product_data = product_serializer.data
    #         return Response("user added")
    #     else:
    #         
    #         return Response("error occured")

class CompanyProductviewset(viewsets.ModelViewSet):
    model = CompanyProduct
    queryset = CompanyProduct.objects.all()
    serializer_class = CompanyProductSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('product_name__product_name')


class CompanyProductWithoutPaginationviewset(viewsets.ModelViewSet):
    model = CompanyProduct
    queryset = CompanyProduct.objects.all()
    serializer_class = CompanyProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name']



class CompanyDivissionProductWithoutPagination(viewsets.ModelViewSet):
    model = CompanyDivisionProduct
    queryset = CompanyDivisionProduct.objects.all()
    serializer_class = CompanyDivisionProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_name__id', 'company_name', 'id','division_name']

    
class CompanyDivisionProductViewset(viewsets.ModelViewSet):
    model = CompanyDivisionProduct
    queryset = CompanyDivisionProduct.objects.all()
    serializer_class = CompanyDivisionProductSerializers
    # permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_name', 'id','division_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('product_name__product_name')


    # @action(detail=False, methods=['post'])
    def create(self, request, *args, **kwargs):
        data = product_data_transmission(request)
        serializer = CompanyDivisionProductSerializers(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(
                {'error':serializer.errors},
                status=status.HTTP_400_BAD_REQUEST)
        

    # @action(detail=True, methods=['put'])
    def update(self, request, *args, **kwargs):
        company_division_product_id = kwargs.get('pk')
        company_division_product_instance = CompanyDivisionProduct.objects.get(
            id=company_division_product_id
        )
        data = product_data_transmission(request)
        serializer = CompanyDivisionProductSerializers(
            company_division_product_instance,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def search_product(self, request, *args, **kwargs):
        search_data = CompanyWiseTrigramSearch(request.data.get('search'),
                             'CompanyDivisionProduct',
                             ['product_name__product_name',
                              'product_name__product_molecular_name',],
                              'Product',
                              request.data.get('company_id')
                              )
        serializer = self.get_serializer(search_data.search(), many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([])
        

    # @action(detail=True, methods=['post'])
    # def destroy_product_of_company_and_division(self, request, *args, **kwargs):
    #     company_division_product_instance = CompanyDivisionProduct.objects.get(
    #         id=kwargs.get('pk')
    #     )
    #     product_instance = Product.objects.get(
    #         id=company_division_product_instance.product_name.id
    #         )
    #     product_instance.delete()
    #     return Response("data deleted successfully")


# class CompanyMpoWiseProductViewset(viewsets.ModelViewSet):
#     model = CompanyMpoWiseProduct
#     queryset = CompanyMpoWiseProduct.objects.all()
#     serializer_class = CompanyMpoWiseProductSerializers
#     pagination_class = CustomPagination
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['product_name__id']

#     @action(detail=False, methods=['post'])
#     def create_product_with_mpo_and_division(self, request, *args, **kwargs):
#         data = product_data_transmission(request)
#         serializer = CompanyDivisionProductSerializers(data = data)
#         if serializer.is_valid():
#             serializer.save()
#             product=serializer.data.get('product_name')
#             company_mpo_data = {
#                 'product_name': product.get('id'),
#                 'company_name':data.get('company_name'),
#                 'mpo_name':data.get('mpo_name')
#             }
#             mpo_serializer = CompanyMpoWiseProductSerializers(
#                 data=company_mpo_data
#                 )
#             if mpo_serializer.is_valid():
#                 mpo_serializer.save()
#                 return Response({'data':mpo_serializer.data,
#                 'data2':serializer.data})
#             else:
#                 
#                 # return Response(mpo_serializer.errors)

#             return Response(serializer.data)
#         else:
#             
#             return Response(serializer.errors)
            
#     @action(detail=True, methods=['put'])
#     def update_product_with_mpo_and_division(self, request, *args, **kwargs):
#         
#         company_division_product_id = kwargs.get('pk')
#         company_division_product_instance = CompanyDivisionProduct.objects.get(
#             id=company_division_product_id
#         )
#         data = product_data_transmission(request)
#         serializer = CompanyDivisionProductSerializers(
#             company_division_product_instance,
#             data=data
#         )
#         if serializer.is_valid():
#             serializer.save()
#             product=serializer.data.get('product_name')
#             
#             CompanyMpoWiseProduct.objects.filter(product_name=product['id']).delete()
#             company_mpo_data = {
#                 'product_name': product.get('id'),
#                 'company_name':data.get('company_name'),
#                 'mpo_name':data.get('mpo_name')
#             }
#             
#             mpo_serialzier = CompanyMpoWiseProductSerializers(
#                 data=company_mpo_data
#             )
#             
#             
#             if mpo_serialzier.is_valid():
#                 mpo_serialzier.save()
#                 
#             else:
#                 
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
            
#     @action(detail=False, methods=['post'])
#     def search_product(self, request, *args, **kwargs):
#         query = request.data.get('search')
#         result = (CompanyDivisionProduct.objects.annotate(
#                         similarity=Greatest(
#                             TrigramSimilarity('company_name__company_name', query),
#                             TrigramSimilarity('product_name__product_name', query),
#                             TrigramSimilarity(
#                                 'product_name__product_molecular_name', query),
#                     )).filter(
#                         Q(company_name__company_name__trigram_similar=query) |
#                         Q(product_name__product_name__trigram_similar=query) |
#                         Q(product_name__product_molecular_name=query)
#                         ,similarity__gt=0.1)).order_by('-similarity')
#         
#         serializer = self.get_serializer(result, many=True)
#         return Response(serializer.data)

        # mpo_name = request.data.get('mpo_name')
        # division_name = request.data.get('division_name')
        # company_name = get_user_from_access(request.data.get('access'))
        # product_data = {
        #     'product_name': request.data.get('product_name'),
        #     'product_molecular_name': request.data.get('product_molecular_name'),
        #     'product_price_per_strip_in_mrp': request.data.get('product_price_per_strip_in_mrp'),
        #     'product_price_for_stockist': request.data.get('product_price_for_stockist'),
        # }
        # product_serializer = ProductAddSerializers(data=product_data)
        # if product_serializer.is_valid():
        #     product_serializer.save()
        #     
        #     product_data = product_serializer.data
        #     company_product_data = {
        #     'company_name': company_name['company_name'],
        #     'product_name': product_data.get('id')
        #     }
        #     
        #     company_product_serializer = CompanyProductSerializer(
        #         data=company_product_data
        #     )
        #     company_division_product_data = {
        #         'company_name': company_name,
        #         'division_name': division_name,
        #         'product_name': product_data.get('id')
        #     } 
        #     company_division_product_serializer = CompanyDivisionProductSerializers(data=company_division_product_data)
        #     if company_product_serializer.is_valid():
        #         company_product_serializer.save()
        #         return Response("product addeed")
        #     elif company_division_product_serializer.is_valid():
        #         company_division_product_serializer.save()
        #         return Response("product added successfully")
        #     else:
        #         
        #         
        #         return Response("product error")
    def bulk_create(self,request):
        
        datas = request.data.get('wholedata')


@api_view(['POST'])
# @paginate_json_response()
def get_all_ordered_product_of_chemist(request):
    data = []
    mpo_shift_wise_dcr_instance = [i.dcr.dcr.id for i in MpoWiseShiftwiseDcrForChemist.objects.filter(
        dcr__dcr__visited_chemist=request.data.get('chemist_id')
    )]
    chemist_instance = CompanyWiseChemist.objects.get(id=request.data.get('chemist_id'))
    dcr_instance = [i.ordered_product for i in DcrForChemistProduct.objects.filter(dcr_id__in=mpo_shift_wise_dcr_instance)]
    ordered_product_information_map =ChemistOrderedProductInformationMap.objects.filter(
        product_id__in=dcr_instance)
    for k in ordered_product_information_map:
        product_instance = CompanyProduct.objects.get(id=k.product_id.id)
        ordered_product_information = ChemistOrderedProductInformation.objects.get(id=k.information_id.id)
        if(ordered_product_information.select_the_stockist):
            stockist_instance = CompanyStockist.objects.get(
                        id=ordered_product_information.select_the_stockist_id)
            data.append({'chemist_name':chemist_instance.chemist_name.chemist_name,
                                 'product_name':product_instance.product_name.product_name,
                                 'stockist_name':stockist_instance.stockist_name.stockist_name,
                                 'ordered_quantity':ordered_product_information.ordered_quantity})
    response_data = {
        'results':data
    }
    return JsonResponse(data=response_data,
                            status=201,headers={
                                'content_type':'application/json'
                            }, safe=False)

@api_view(['POST'])
# @paginate_json_response()
def get_stockist_ordered_product(request):
    data = []
    mpo_shift_wise_dcr_instance =[i.dcr.dcr.id for i in MpoWiseShiftwiseDcrForStockist.objects.filter(
        dcr__dcr__visited_stockist=request.data.get('stockist_id')
    )]
    stockist_instance = CompanyStockist.objects.get(id=request.data.get('stockist_id'))
    dcr_for_stockist_ordered_product_instance = DcrForStockistOrderedProduct.objects.filter(
            dcr_id__in=mpo_shift_wise_dcr_instance)
    for j in dcr_for_stockist_ordered_product_instance:
        stockist_product_instance = StockistOrderedProduct.objects.get(
            id=j.ordered_product.id)
        data.append({'stockist_name':stockist_instance.stockist_name.stockist_name,
                        'ordered_product':stockist_product_instance.ordered_product.product_name.product_name,
                        'ordered_quantity':stockist_product_instance.ordered_quantity})
    response_data = {
        'results':data
    }
    return JsonResponse(response_data,
                        status=200)