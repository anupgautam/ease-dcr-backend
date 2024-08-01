from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import (AllowAny)

from Account.pagination import CustomPagination
from Chemist.models import (
    Chemist,
    ChemistCategory,
    ChemistCompanyArea,
    ChemistWorkingArea,
    CompanyChemistCategory,
    CompanyWiseChemist)
from Chemist.serializers import (
    AddChemistSerializer,
    ChemistCategorySerializer,
    ChemistCompanyAreaSerializer,
    ChemistSerializer,
    CompanyChemistCategorySerializer,
    CompanyWiseChemistSerializer,
    WorkingAreaSerializer)
from Chemist.utils import (chemsit_data_transmission,
                           chemist_category_data)
from Doctors.search import CompanyWiseTrigramSearch
from utility.action_permissions import (
    ADMIN_CREATE_UPDATE_VIEW_AUTHENTICATED,
    AUTHENTICATED_ALL)


class ActionBasedPermission(AllowAny):
    """
    Grant or deny access to a view, based on a mapping in view.action_permissions
    """
    def has_permission(self, request, view):
        for klass, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return klass().has_permission(request, view)
        return False

class ChemistViewSet(viewsets.ModelViewSet):
    queryset = Chemist.objects.all()
    pagination_class = CustomPagination
    action_permissions = AUTHENTICATED_ALL

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('chemist_name')

    def create(self, request, *args, **kwargs):
        chemist_data = chemsit_data_transmission(request)
        serializer = self.get_serializer_class()(data=chemist_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data},
            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):
        if self.action == "create":
            return AddChemistSerializer
        else:
            return ChemistSerializer

    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')     
        chemist_instance = Chemist.objects.get(id=id)
        data = chemsit_data_transmission(request)
        serializer = AddChemistSerializer(chemist_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ChemistCategoryViewSet(viewsets.ModelViewSet):
    queryset = ChemistCategory.objects.all()
    serializer_class = ChemistCategorySerializer
    action_permissions = ADMIN_CREATE_UPDATE_VIEW_AUTHENTICATED


class CompanyWiseChemistWithoutPagination(viewsets.ModelViewSet):
    queryset = CompanyWiseChemist.objects.all()
    serializer_class = CompanyWiseChemistSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'company_name',
        'chemist_name__id',
        'chemist_name__chemist_territory',
        'mpo_name']
    action_permissions = AUTHENTICATED_ALL


class CompanyWiseChemistViewSet(viewsets.ModelViewSet):
    queryset = CompanyWiseChemist.objects.all()
    serializer_class = CompanyWiseChemistSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'id',
        'company_name',
        'chemist_name__id',
        'chemist_name__chemist_territory',
        'mpo_name']
    action_permissions = AUTHENTICATED_ALL

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('chemist_name__chemist_name')
    
    @action(detail=False, methods=['post'])
    def search_chemist(self, request, *args, **kwargs):
        search_data = CompanyWiseTrigramSearch(request.data.get('search'),
                             'CompanyWiseChemist',
                             ['chemist_name__chemist_name',
                              'chemist_name__chemist_address',
                              'chemist_name__chemist_phone_number'],
                              'Chemist',
                              request.data.get('company_id')
                              )
        serializer = self.get_serializer(search_data.search(), many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([])


class ChemistWorkingAreaViewset(viewsets.ModelViewSet):
    queryset = ChemistWorkingArea.objects.all()
    serializer_class = WorkingAreaSerializer
    action_permissions = AUTHENTICATED_ALL


class CompanyChemistCategoryViewset(viewsets.ModelViewSet):
    queryset = CompanyChemistCategory.objects.all()
    serializer_class = CompanyChemistCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name']
    action_permissions = ADMIN_CREATE_UPDATE_VIEW_AUTHENTICATED

    def create(self, request, *args, **kwargs):
        data = chemist_category_data(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = CompanyChemistCategory.objects.get(
            id=kwargs.get('pk'))
        category_instance = ChemistCategory.objects.get(
            id=instance.category_name.id)
        category_instance.delete()
        return super().destroy(request, *args, **kwargs)


class ChemistCompanyAreaViewset(viewsets.ModelViewSet):
    queryset = ChemistCompanyArea.objects.all()
    serializer_class = ChemistCompanyAreaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name']
    action_permissions = AUTHENTICATED_ALL
