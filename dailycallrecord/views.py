from rest_framework import viewsets
from rest_framework.decorators import action
from dailycallrecord.serializers import *
from dailycallrecord.models import *
from .utils import dcr_for_doctor_data_transmission
from .utils import dcr_for_chemist_data_transmission
from .utils import dcr_for_stockist_data_transmission
from .utils import stockist_ordered_product_information
from rest_framework.response import Response
from django.db.models import Count
from .graph import OptimizedGraph
from rest_framework.decorators import api_view
from django.db.models import Max
from .graph import get_maximum_ordered_product
from Account.pagination import CustomPagination
from utility.logic import RetrieveLogicID, RetrieveLogicIDSelect,formdata_application_json
from utility.get_template_data import get_template_data

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated)
from rest_framework import status
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.views import APIView
from rest_framework import filters


@api_view(['GET','POST'])
def get_maximum_ordered_product_by_chemist_and_stockist(request):
    
    return JsonResponse(get_maximum_ordered_product(request), status=201, headers={
            'content_type':'application/json'})


class RewardViewset(viewsets.ModelViewSet):
    serializer_class = RewardsSerializer
    queryset = Rewards.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['company_name']


class DcrForDoctorViewset(viewsets.ModelViewSet):
    serializer_class = DcrForDoctorSerializer
    queryset = DcrForDoctor.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DcrForDoctorRewardsMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForDoctorRewardsMapSerializer
    queryset = DcrForDoctorRewardsMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


class DcrForDoctorCompanyProductMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForDoctorCompanyProductMapSerializer
    queryset = DcrForDoctorCompanyProductMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]



class DcrForDoctorCompanyRolesMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForDoctorCompanyRolesMapSerializer
    queryset = DcrForDoctorCompanyRolesMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA = [
        {
    'model': CompanyProduct,
    'mapped_model': DcrForDoctorCompanyProductMap,
    'fk_original': 'dcr_id',
    'fk_map': 'company_product_id',
    'serializer': CompanyProductSerializerWithoutToRepresentation,
    'mapped_serializer':DcrForDoctorCompanyProductMapSerializer,
    'model_field_name': 'company_product'
    },
        {
    'model': Rewards,
    'mapped_model': DcrForDoctorRewardsMap,
    'fk_original': 'dcr_id',
    'fk_map': 'reward_id',
    'serializer': RewardsSerializer,
    'mapped_serializer':DcrForDoctorRewardsMapSerializer,
    'model_field_name': 'rewards'
    },
        {
    'model': CompanyUserRole,
    'mapped_model': DcrForDoctorCompanyRolesMap,
    'fk_original': 'dcr_id',
    'fk_map': 'roles_id',
    'serializer': CompanyUserRoleSerializersWithoutToRepresentation,
    'mapped_serializer':DcrForDoctorCompanyRolesMapSerializer,
    'model_field_name': 'company_roles'
    },
]
class DCRProductRewardsRolesViewset(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    serializer_class = DCRProductRewardsRolesSerializer
    action_permissions = {
      AllowAny: ['update', 'partial_update', 'destroy', 'create', 'retrieve', 'list'],
        # IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
        # AllowAny: ['retrieve', 'list']
    }
    def retrieve(self, request, pk=None):
        if pk is None or pk == 'null':
            return Response(
                data={'error': 'null primery key value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        DATA = get_template_data(
            DcrForDoctor,
            DcrForDoctorSerializer,
            DCR_FOR_DOCTOR_PRODUCT_ROLES_REWARDS_DATA
        )
        data = RetrieveLogicID(DATA, pk).retrieve()
        sending_data = data.copy()
        if sending_data['visited_doctor'] is None:
            sending_data['visited_doctor'] = None
        else:
            sending_data['visited_doctor'] = CompanyWiseDoctor.objects.get(id=data.get('visited_doctor')).__dict__
        if sending_data['visited_area'] is None:
            sending_data['visited_area'] = None
        else:
            sending_data['visited_area'] = CompanyMPOArea.objects.get(id=data.get('visited_area')).__dict__
        serializer = self.serializer_class(data=sending_data,
                                           context={'request':'GET'})
        if serializer.is_valid():
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND)
 
    def create(self, request):
        serializer = self.serializer_class(
                        data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        context = request.data.get('context')
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        if 'visited_doctor' in sending_data:
            sending_data['visited_doctor'] = CompanyWiseDoctor.objects.get(id=data.get('visited_doctor')).__dict__
        else:
            sending_data['visited_doctor'] = None
        if 'visited_area' in sending_data:
            sending_data['visited_area'] = CompanyMPOArea.objects.get(id=data.get('visited_area')).__dict__
        else:
            sending_data['visited_area'] = None
        serializer = self.serializer_class(
            instance = DcrForDoctor.objects.get(id=pk),
            data=sending_data,
            partial=True,
            context=data.get('context'))
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        context = request.data.get('context')
        id = request.data.get('id')
        serializer = self.serializer_class(
            instance = DcrForDoctor.objects.get(id=id),
            data=request.data,
            context=context)
        if serializer.is_valid():
            deleted_return = serializer.delete(request.data)
            # for data in deleted_return['holiday_package_itinerary']:
            #     data['itinerary_image'] = None
            serializer1 = self.serializer_class(data=deleted_return)
            if serializer1.is_valid():
                return Response(
                    data=serializer1.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer1.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class MpoWiseShiftWiseDcrForDoctorViewset(viewsets.ModelViewSet):
    serializer_class = MpoWiseShiftWiseDcrForDoctorSerializer
    queryset = MpoWiseShiftwiseDcrForDoctor.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mpo_name',
                        'id',
                        'dcr__dcr__month',
                        'dcr__dcr__year',
                        'dcr__dcr__date',
                        'dcr__dcr__id',
                        'dcr__dcr__visited_doctor__company_name',
                        ]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('dcr__dcr__date')

    def create(self, request, *args, **kwargs):
        data = dcr_for_doctor_data_transmission(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)
    def update(self, request, *args, **kwargs):
        mpo_wise_dcr_for_doctor = MpoWiseShiftwiseDcrForDoctor.objects.get(
            id=kwargs.get('pk')
        )
        data = dcr_for_doctor_data_transmission(request)
        serializer = self.serializer_class(
            mpo_wise_dcr_for_doctor,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class MpoWiseShiftWiseDcrForDoctorWithOutPaginationViewset(viewsets.ModelViewSet):
    serializer_class = MpoWiseShiftWiseDcrForDoctorSerializer
    queryset = MpoWiseShiftwiseDcrForDoctor.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mpo_name',
                        'id',
                        'dcr__dcr__month',
                        'dcr__dcr__year',
                        'dcr__dcr__date',
                        'dcr__dcr__id',
                        'dcr__dcr__visited_doctor__company_name',
                        ]

class ShiftwiseDcrForDoctorViewset(viewsets.ModelViewSet):
    serializer_class = ShiftwiseDcrForDoctorSerializer
    queryset = ShiftWiseDcrForDoctor.objects.all()


class ChemistOrderedProductViewset(viewsets.ModelViewSet):
    serializer_class = ChemistOrderedProductSerializer
    queryset = ChemistOrderedProduct.objects.all()

    
class DcrForChemsitViewset(viewsets.ModelViewSet):
    serializer_class = DcrForChemistSerializer
    queryset = DcrForChemist.objects.all()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DcrForChemistProductViewset(viewsets.ModelViewSet):
    serializer_class = DcrForChemistProductSerializer
    queryset = DcrForChemistProduct.objects.all()


class DcrForChemistPromotedProductMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForChemistPromotedProductMapSerializer
    queryset = DcrForChemistPromotedProductMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


class DcrForChemistRewardsMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForChemistRewardsMapSerializer
    queryset = DcrForChemistRewardsMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


class DcrForChemistCompanyRolesMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForChemistCompanyRolesMapSerializer
    queryset = DcrForChemistCompanyRolesMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


DCR_ORDERED_PRODUCT_INFORMATION = [
            {
    'model': ChemistOrderedProductInformation,
    'mapped_model': ChemistOrderedProductInformationMap,
    'fk_original': 'product_id',
    'fk_map': 'information_id',
    'serializer': ChemistOrderedProductInformationSerializer,
    'mapped_serializer':ChemistOrderedProductInformationMapSerializer,
    'model_field_name': 'product_information'
    },
]

class DCRChemistOrderedProductInformationViewset(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    serializer_class = DCRChemistOrderedProductInformationSerializer
    action_permissions = {
      AllowAny: ['update', 'partial_update', 'destroy', 'create', 'retrieve', 'list'],
        # IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
        # AllowAny: ['retrieve', 'list']
    }
    def retrieve(self, request, pk=None):
        if pk is None or pk == 'null':
            return Response(
                data={'error': 'null primery key value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        DATA = get_template_data(
            CompanyProduct,
            ChemistOrderedProductInformationSerializer,
            DCR_ORDERED_PRODUCT_INFORMATION
        )
        data = RetrieveLogicID(DATA, pk).retrieve()
        sending_data = data.copy()
        # sending_data['ordered_product'] = CompanyProduct.objects.get(id=data.get('ordered_product')).__dict__
        # data = RetrieveLogicID(DATA, pk).retrieve()
        serializer = self.serializer_class(data=sending_data)
        if serializer.is_valid():
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND)
 
    def create(self, request):
        context = request.data.get('context')
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        # if 'ordered_product' in sending_data:
        #     sending_data['ordered_product'] = ChemistOrderedProduct.objects.get(id=data.get('ordered_product')).__dict__
        # else:
        #     sending_data['ordered_product'] = None
        serializer = self.serializer_class(
                        data=sending_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        context = request.data.get('context')
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        # if 'ordered_product' in sending_data:
        #     sending_data['ordered_product'] = CompanyProduct.objects.get(id=data.get('ordered_product')).__dict__
        # else:
        #     sending_data['ordered_product'] = None
        serializer = self.serializer_class(
            instance = CompanyProduct.objects.get(id=pk),
            data=sending_data,
            partial=True,
            context=data.get('context'))
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        data = formdata_application_json(request.data)
        serializer = self.serializer_class(
            instance = CompanyProduct.objects.get(id=id),
            data=request.data,
            context=data.get('context'))
        if serializer.is_valid():
            deleted_return = serializer.delete(request.data)
            # for data in deleted_return['holiday_package_itinerary']:
            #     data['itinerary_image'] = None
            serializer1 = self.serializer_class(data=deleted_return)
            if serializer1.is_valid():
                return Response(
                    data=serializer1.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer1.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA = [
        {
    'model': CompanyProduct,
    'mapped_model': DcrForChemistPromotedProductMap,
    'fk_original': 'dcr_id',
    'fk_map': 'company_product_id',
    'serializer': CompanyProductSerializerWithoutToRepresentation,
    'mapped_serializer':DcrForChemistPromotedProductMapSerializer,
    'model_field_name': 'company_product'
    },
        {
    'model': Rewards,
    'mapped_model': DcrForChemistRewardsMap,
    'fk_original': 'dcr_id',
    'fk_map': 'reward_id',
    'serializer': RewardsSerializer,
    'mapped_serializer':DcrForChemistRewardsMapSerializer,
    'model_field_name': 'rewards'
    },
        {
    'model': CompanyUserRole,
    'mapped_model': DcrForChemistCompanyRolesMap,
    'fk_original': 'dcr_id',
    'fk_map': 'roles_id',
    'serializer': CompanyUserRoleSerializersWithoutToRepresentation,
    'mapped_serializer':DcrForChemistCompanyRolesMapSerializer,
    'model_field_name': 'company_roles'
    },
    {
    'model': CompanyProduct,
    'mapped_model': DcrForChemistProduct,
    'fk_original': 'dcr_id',
    'fk_map': 'ordered_product',
    'serializer': CompanyProductSerializerWithoutToRepresentation,
    'mapped_serializer':DcrForChemistProductSerializer,
    'model_field_name': 'ordered_products'
    },
    
]


class DCRChemistProductRewardsRolesViewset(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    serializer_class = DCRChemistProductRewardsRolesSerializer
    action_permissions = {
      AllowAny: ['update', 'partial_update', 'destroy', 'create', 'retrieve', 'list'],
        # IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
        # AllowAny: ['retrieve', 'list']
    }
    def retrieve(self, request, pk=None):
        if pk is None or pk == 'null':
            return Response(
                data={'error': 'null primery key value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        DATA = get_template_data(
            DcrForChemist,
            DcrForChemistSerializer,
            DCR_FOR_CHEMIST_PRODUCT_ROLES_REWARDS_DATA
        )
        data = RetrieveLogicIDSelect(DATA, pk, ['visited_chemist', 'visited_area',]).retrieve()
        # data = RetrieveLogicID(DATA, pk).retrieve()
        sending_data = data.copy()
        if sending_data['visited_chemist'] is None :
            sending_data['visited_chemist'] = None
        else:
            sending_data['visited_chemist'] = CompanyWiseChemist.objects.get(id=data.get('visited_chemist')).__dict__
        if sending_data['visited_area'] is None:
            sending_data['visited_area'] = None
        else:
            sending_data['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__

        serializer = self.serializer_class(data=sending_data)
        if serializer.is_valid():
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND)
 
    def create(self, request):
        print("hamro data",request.data)
        context = request.data.get('context')
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        if 'visited_chemist' in sending_data:
            sending_data['visited_chemist'] = CompanyWiseChemist.objects.get(id=data.get('visited_chemist')).__dict__
        else:
            sending_data['visited_chemist'] = None
        if 'visited_area' in sending_data:
            sending_data['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
        else:
            sending_data['visited_area'] = None
        serializer = self.serializer_class(
                        data=sending_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        context = request.data.get('context')
        if context is None:
            context = {
        "company_product":"select",
        "company_roles":"select",
        "rewards":"select",
        "ordered_products":"select"
    }
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        if sending_data:
            if sending_data['visited_chemist']:
                sending_data['visited_chemist'] = CompanyWiseChemist.objects.get(id=data.get('visited_chemist')).__dict__
            else:
                sending_data['visited_chemist'] = None
            if sending_data['visited_area']:
                sending_data['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
            else:
                sending_data['visited_area'] = None
            if sending_data['date']:
                sending_data['date'] = sending_data['date']
            else:
                sending_data['date'] = None
            serializer = self.serializer_class(
                instance = DcrForChemist.objects.get(id=pk),
                data=sending_data,
                partial=True,
                context=context)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response("please send the data")

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        context = request.data.get('context')
        serializer = self.serializer_class(
            instance = DcrForChemist.objects.get(id=id),
            data=request.data,
            context=context
            )
        if serializer.is_valid():
            deleted_return = serializer.delete(request.data)
            # for data in deleted_return['holiday_package_itinerary']:
            #     data['itinerary_image'] = None
            serializer1 = self.serializer_class(data=deleted_return)
            if serializer1.is_valid():
                return Response(
                    data=serializer1.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer1.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        

class ShiftwiseDcrForChemistViewset(viewsets.ModelViewSet):
    serializer_class = ShiftwiseDcrForChemistSerializer
    queryset = ShiftWiseDcrForChemist.objects.all()


class MpoWiseShiftWiseDcrForChemistViewset(viewsets.ModelViewSet):
    serializer_class = MpoWiseShiftWiseDcrForChemistSerializer
    queryset = MpoWiseShiftwiseDcrForChemist.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'mpo_name',
        'dcr__dcr__month',
        'dcr__dcr__year',
        'dcr__dcr__date',
        'dcr__dcr__id',
        'dcr__dcr__visited_chemist__company_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('dcr__dcr__date')

    def create(self, request, *args, **kwargs):
        data = dcr_for_chemist_data_transmission(request)
        serializer = self.serializer_class(data=data,)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)
    def update(self, request, *args, **kwargs):
        mpo_wise_dcr_for_chemist = MpoWiseShiftwiseDcrForChemist.objects.get(
            id=kwargs.get('pk')
        )
        data = dcr_for_chemist_data_transmission(request)
        serializer = self.serializer_class(
            mpo_wise_dcr_for_chemist,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA = [
        {
    'model': Rewards,
    'mapped_model': DcrForStockistRewardsMap,
    'fk_original': 'dcr_id',
    'fk_map': 'reward_id',
    'serializer': RewardsSerializer,
    'mapped_serializer':DcrForStockistRewardsMapSerializer,
    'model_field_name': 'rewards'
    },
        {
    'model': CompanyUserRole,
    'mapped_model': DcrForStockistCompanyRolesMap,
    'fk_original': 'dcr_id',
    'fk_map': 'roles_id',
    'serializer': CompanyUserRoleSerializersWithoutToRepresentation,
    'mapped_serializer':DcrForStockistCompanyRolesMapSerializer,
    'model_field_name': 'company_roles'
    },
    #     {
    # 'model': StockistOrderedProduct,
    # 'mapped_model': DcrForStockistOrderedProduct,
    # 'fk_original': 'dcr_id',
    # 'fk_map': 'ordered_product',
    # 'serializer': StockistOrderedProductSerializer,
    # 'mapped_serializer':DcrForStockistOrderedProductSerializer,
    # 'model_field_name': 'ordered_products'
    # }
]

class StockistOrderedProductViewset(viewsets.ModelViewSet):
    serializer_class = StockistOrderedProductSerializer
    queryset = StockistOrderedProduct.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


class DcrForStockistViewset(viewsets.ModelViewSet):
    serializer_class = DcrForStockistSerializer
    queryset = DcrForStockist.objects.all()
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DCRStockistProductRewardsRolesViewset(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']
    serializer_class = DCRStockistProductRewardsRolesSerializer
    action_permissions = {
      AllowAny: ['update', 'partial_update', 'destroy', 'create', 'retrieve', 'list'],
        # IsAdminUser: ['update', 'partial_update', 'destroy', 'create'],
        # AllowAny: ['retrieve', 'list']
    }
    def retrieve(self, request, pk=None):
        if pk is None or pk == 'null':
            return Response(
                data={'error': 'null primery key value'},
                status=status.HTTP_400_BAD_REQUEST
            )
        DATA = get_template_data(
            DcrForStockist,
            DcrForStockistSerializer,
            DCR_FOR_STOCKIST_PRODUCT_ROLES_REWARDS_DATA
        )
        data = RetrieveLogicIDSelect(DATA, pk, ['visited_stockist', 'visited_area',]).retrieve()
        sending_data = data.copy()
        # sending_data['visited_stocksit'] = CompanyStockist.objects.get(id=data.get('visited_stockist')).__dict__
        if sending_data['visited_stockist'] is None:
            sending_data['visited_stockist'] = None
        else:
            sending_data['visited_stockist'] = CompanyStockist.objects.get(id=data.get('visited_stockist')).__dict__
        if sending_data['visited_area'] is None:
            sending_data['visited_area'] = None
        else:
            sending_data['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
        serializer = self.serializer_class(data=sending_data
                                        )
        if serializer.is_valid():
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_404_NOT_FOUND)
 
    def create(self, request):
        context = request.data.get('context')
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        if 'visited_stockist' in sending_data:
            sending_data['visited_stockist'] = CompanyStockist.objects.get(id=data.get('visited_stockist')).__dict__
        else:
            sending_data['visited_stockist'] = None
        if 'visited_area' in sending_data:
            sending_data['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
        else:
            sending_data['visited_area'] = None
        serializer = self.serializer_class(
                        data=sending_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK)
    
    def partial_update(self, request, pk=None):
        context = request.data.get('context')
        if context is None:
            context = {
        "company_roles":"select",
        "rewards":"select",
        # "ordered_products":"select"
    }
        data = formdata_application_json(request.data)
        sending_data = request.data.copy()
        if sending_data:
            if sending_data.get('visited_stockist'):
                sending_data['visited_stockist'] = CompanyStockist.objects.get(id=data.get('visited_stockist')).__dict__
            else:
                sending_data['visited_stockist'] = None
            if sending_data.get('visited_area'):
                sending_data['visited_area'] = CompanyArea.objects.get(id=data.get('visited_area')).__dict__
            else:
                sending_data['visited_area'] = None
            if sending_data.get('date'):
                sending_data['date'] = sending_data['date']
            else:
                sending_data['date'] = None
            serializer = self.serializer_class(
                instance = DcrForStockist.objects.get(id=pk),
                data=sending_data,
                partial=True,
                context=context)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(
                    data=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK)
        else:
            return Response("please send data")

    def destroy(self, request, *args, **kwargs):
        id = request.data.get('id')
        serializer = self.serializer_class(
            instance = DcrForStockist.objects.get(id=id),
            data=request.data)
        if serializer.is_valid():
            deleted_return = serializer.delete(request.data)
            # for data in deleted_return['holiday_package_itinerary']:
            #     data['itinerary_image'] = None
            serializer1 = self.serializer_class(data=deleted_return)
            if serializer1.is_valid():
                return Response(
                    data=serializer1.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data=serializer1.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class DcrForStockistOrderedProductViewset(viewsets.ModelViewSet):
    serializer_class = DcrForStockistOrderedProductSerializer
    queryset = DcrForStockistOrderedProduct.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dcr_id']
    def create(self, request, *args, **kwargs):
        data = stockist_ordered_product_information(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def update(self, request, *args, **kwargs):
        instance = DcrForStockistOrderedProduct.objects.get(id=kwargs.get('pk'))
        data = stockist_ordered_product_information(request)
        serializer = self.serializer_class(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        instance = DcrForStockistOrderedProduct.objects.get(
            id=kwargs.get('pk'))
        stockist_ordered_product_instance = StockistOrderedProduct.objects.get(
            id=instance.ordered_product.id
        )
        stockist_ordered_product_instance.delete()
        return super().destroy(request, *args, **kwargs)
    

class DcrForStockistRewardsMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForStockistRewardsMapSerializer
    queryset = DcrForStockistRewardsMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]


class DcrForStockistCompanyRolesMapViewset(viewsets.ModelViewSet):
    serializer_class = DcrForStockistCompanyRolesMapSerializer
    queryset = DcrForStockistCompanyRolesMap.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]

class ShiftwiseDcrForStockistViewset(viewsets.ModelViewSet):
    serializer_class = ShiftwiseDcrForStockistSerializer
    queryset = ShiftWiseDcrForStockist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
                        'id',
                        'dcr_id',
                       ]

class MpoWiseShiftWiseDcrForStockistViewset(viewsets.ModelViewSet):
    serializer_class = MpoWiseShiftWiseDcrForStockistSerializer
    queryset = MpoWiseShiftwiseDcrForStockist.objects.all()
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mpo_name',
                        'dcr__dcr__month',
                        'dcr__dcr__year',
                        'dcr__dcr__date',
                        'dcr__dcr__id',
                        'dcr__dcr__visited_stockist__company_name'
                        ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('dcr__dcr__date')

    def create(self, request, *args, **kwargs):
        data = dcr_for_stockist_data_transmission(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors)
    def update(self, request, *args, **kwargs):
        # max_quantity = get_maximum_ordered_product()
        mpo_wise_dcr_for_stockist = MpoWiseShiftwiseDcrForStockist.objects.get(
            id=kwargs.get('pk')
        )
        data = dcr_for_stockist_data_transmission(request)
        serializer = self.serializer_class(
            mpo_wise_dcr_for_stockist,
            data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)