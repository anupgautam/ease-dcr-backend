from Stat.utils import get_nepali_dates_for_month
from otherroles.models import HigherOrderDCR
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db.models import Count, Sum
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from DCRUser.models import CompanyUserRole
from Expenses.models import LeaveApplication
from Expenses.utils import get_all_leave_dates_from_month
from Mpo.models import CompanyMPOAreaTourPlan, CompanyMpoTourPlan
from Mpo.utils import get_unplanned_tour_plan_dates_month

from Stat.models import CompanyDCRTourPlanValidity, MPOMissedCallModel
from Company.models import Company, CompanyRoles
from Product.models import CompanyProduct
from Stockist.models import CompanyStockist
from Doctors.models import CompanyWiseDoctor    
from Chemist.models import CompanyWiseChemist
from Stat.serializers import CompanyDCRTourPlanValiditySerializers, MPOMissedCallSerializers
from Product.serializers import CompanyProductSerializer
from Chemist.serializers import CompanyWiseChemistSerializer
from Doctors.serializers import CompanyWiseDoctorSerializer
from Stockist.serializers import CompanyStockistSerializers
from dailycallrecord.serializers import StockistOrderedProductSerializerWithToRepresentation
from dailycallrecord.models import (DcrForChemistCompanyRolesMap, DcrForDoctorCompanyRolesMap, DcrForStockistCompanyRolesMap, MpoWiseShiftwiseDcrForChemist,
                                    MpoWiseShiftwiseDcrForStockist,
                                    MpoWiseShiftwiseDcrForDoctor,
                                    StockistOrderedProduct,
                                    DcrForStockistOrderedProduct,
                                    DcrForDoctorCompanyProductMap,
                                    DcrForChemistPromotedProductMap,
                                    DcrForChemistProduct,
                                    ChemistOrderedProductInformationMap)


def get_most_visited_chemist(company_name):
    most_visited_chemist = MpoWiseShiftwiseDcrForChemist.objects.filter(
        mpo_name__company_name=company_name).values(
        'dcr__dcr__visited_chemist').annotate(
        visit_count=Count('dcr__dcr__visited_chemist')).order_by(
        '-visit_count')[:10]
    if most_visited_chemist:
        visited_chemist_id = [i['dcr__dcr__visited_chemist'] for i in most_visited_chemist]
        visited_chemist = CompanyWiseChemist.objects.filter(id__in=visited_chemist_id)
        return visited_chemist
    else:
        return None
    
    
def get_most_visited_doctor(company_name):
    most_visited_doctor = MpoWiseShiftwiseDcrForDoctor.objects.filter(
        mpo_name__company_name=company_name).values(
        'dcr__dcr__visited_doctor').annotate(
        visit_count=Count('dcr__dcr__visited_doctor')).order_by(
        '-visit_count')[:10]
    if most_visited_doctor:
        visited_doctor_id =[i['dcr__dcr__visited_doctor'] for i in most_visited_doctor]
        visited_doctor = CompanyWiseDoctor.objects.filter(id__in=visited_doctor_id)
        return visited_doctor
    else:
        return None
    

def get_most_visited_stockist(company_name):
    most_visited_stockist = MpoWiseShiftwiseDcrForStockist.objects.filter(
        mpo_name__company_name=company_name).values(
        'dcr__dcr__visited_stockist').annotate(
        visit_count=Count('dcr__dcr__visited_stockist')).order_by(
        '-visit_count')[:10]
    if most_visited_stockist:
        visited_stockist_id = [i['dcr__dcr__visited_stockist'] for i in most_visited_stockist]
        visited_stockist = CompanyStockist.objects.filter(id__in=visited_stockist_id)
        return visited_stockist
    else:
        return None


def get_list_of_most_ordered_products_of_stockist(company_name):
    company_products = CompanyProduct.objects.filter(company_name=company_name)
    if company_products:
        ordered_product_ids = [product for product in company_products]
        top_10_ordered_products = StockistOrderedProduct.objects.filter(
            ordered_product__in=ordered_product_ids).exclude(
            ordered_quantity__isnull=True).order_by(
            '-ordered_quantity')[:10]   
        return top_10_ordered_products

def get_list_of_most_ordered_products_of_chemist(company_name):
    data = []
    company_products = DcrForChemistProduct.objects.filter(
        ordered_product__company_name=company_name
    )
    top_10_products = ChemistOrderedProductInformationMap.objects.filter(
        product_id__in=company_products
    ).exclude(information_id__ordered_quantity__isnull=True).values('product_id').annotate(
        total_ordered_quantity=Sum(
        'information_id__ordered_quantity')).order_by(
        '-total_ordered_quantity')[:10]
    for i in top_10_products:
        instance = DcrForChemistProduct.objects.get(id=i['product_id'])
        data.append({'product_name':instance.ordered_product.product_name.product_name, 'ordered_quantity':i['total_ordered_quantity']})
    return data
    
def get_list_of_most_promoted_products_of_chemist(company_name):
    dcr_ids = MpoWiseShiftwiseDcrForChemist.objects.filter(
        mpo_name__company_name=company_name
    ).values_list('dcr__dcr_id', flat=True)
    promoted_products = DcrForChemistPromotedProductMap.objects.filter(
        dcr_id__in=dcr_ids).values(
        'company_product_id').annotate(
        product_count=Count('company_product_id')).order_by(
        '-product_count')[:10]
    if promoted_products:
        top_10_company_product_ids = [item['company_product_id'] for item in promoted_products]
        top_10_ordered_products = CompanyProduct.objects.filter(id__in=top_10_company_product_ids)
        return top_10_ordered_products
    else:
        return None
    
def get_list_of_most_promoted_products_of_doctor(company_name):
    dcr_ids = MpoWiseShiftwiseDcrForDoctor.objects.filter(
        mpo_name__company_name=company_name
    ).values_list('dcr__dcr_id', flat=True)
    ordered_products = DcrForDoctorCompanyProductMap.objects.filter(
        dcr_id__in=dcr_ids).values(
        'company_product_id').annotate(
        product_count=Count('company_product_id')).order_by(
        '-product_count')[:10]
    if ordered_products:
        top_10_company_product_ids = [item['company_product_id'] for item in ordered_products]
        top_10_ordered_products = CompanyProduct.objects.filter(id__in=top_10_company_product_ids)
        return top_10_ordered_products
    else:
        return None

def get_total_product(company_name):
    return CompanyProduct.objects.filter(
        company_name=company_name
    ).count()

def get_total_doctor(company_name):
    return CompanyWiseDoctor.objects.filter(
        company_name=company_name
    ).count()

def get_total_stockist(company_name):
    return CompanyStockist.objects.filter(
        company_name=company_name
    ).count()

def get_total_chemist(company_name):
    return CompanyWiseChemist.objects.filter(
        company_name=company_name
    ).count()


def get_missed_calls(request):
    company_name = request.data.get('company_name')
    role = request.data.get('role')
    all_company_roles = CompanyRoles.objects.filter(
        company_name=company_name,
        role_name=role
    )
    
@api_view(['POST'])
def get_stat(request):
    if request.data.get('company_name'):
        chemist_serializer = CompanyWiseChemistSerializer(
            get_most_visited_chemist(
            request.data.get('company_name')), many=True)  
        doctor_serializer = CompanyWiseDoctorSerializer(
            get_most_visited_doctor(
            request.data.get('company_name')), many=True)
        stockist_serializer = CompanyStockistSerializers(
            get_most_visited_stockist(
            request.data.get('company_name')), many=True)
        stockist_ordered_product_serializer = StockistOrderedProductSerializerWithToRepresentation(
            get_list_of_most_ordered_products_of_stockist(
            request.data.get('company_name')), many=True)
        doctor_promoted_product = CompanyProductSerializer(
            get_list_of_most_promoted_products_of_doctor(
            request.data.get('company_name')), many=True)
        chemist_promoted_product = CompanyProductSerializer(
            get_list_of_most_promoted_products_of_chemist(
            request.data.get('company_name')), many=True)
        data = {
            'total_number':{
            'total_product':get_total_product(request.data.get('company_name')),
            'total_chemist':get_total_chemist(request.data.get('company_name')),
            'total_stockist':get_total_stockist(request.data.get('company_name')),
            'total_doctor':get_total_doctor(request.data.get('company_name')),
            },
            'most_promoted_product':{
                'chemist':chemist_promoted_product.data,
                'doctor':doctor_promoted_product.data
            },
            'most_ordered_product':{
            'chemist_ordered_product':get_list_of_most_ordered_products_of_chemist(
            request.data.get('company_name')),
            'stockist_ordered_product':stockist_ordered_product_serializer.data
            },
            'company':{
                'stockist':stockist_serializer.data,
                'chemist':chemist_serializer.data,
                'doctor':doctor_serializer.data
            }
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'Error':"Please send the company ID"}, safe=False)


class CompanyDCRTourPlanValidityViewsets(viewsets.ModelViewSet):
    model = CompanyDCRTourPlanValidity
    queryset = CompanyDCRTourPlanValidity.objects.all()
    serializer_class = CompanyDCRTourPlanValiditySerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company']


class MPOMissedCallModelViewsets(viewsets.ModelViewSet):
    model = MPOMissedCallModel
    queryset = MPOMissedCallModel.objects.all()
    serializer_class = MPOMissedCallSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'company_name', 'month', 'year', 'mpo_name']


@api_view(['POST'])
def get_missed_call_data(request):
    month = request.data.get('month')
    company = request.data.get('company')
    year = request.data.get('year')
    get_all_company_user_id = [i for i in CompanyUserRole.objects.filter(company_name=company)]
    for i in get_all_company_user_id:
        unplanned_tour_plan = []
        leaves = []
        if i.role_name.role_name.role_name in ['MPO', 'mpo', 'MPO']:
            leaves = get_all_leave_dates_from_month(year, month, i.id)
            unplanned_tour_plan = get_unplanned_tour_plan_dates_month(year, month, i.id)
        get_month_mpo_tour_plan = CompanyMpoTourPlan.objects.filter(
            mpo_name__id=i.id,
            tour_plan__tour_plan__select_the_month=month,
            tour_plan__tour_plan__select_the_date_id__year=year,
            is_missed_call_calculated=False 
        ).exclude(
            tour_plan__tour_plan__select_the_date_id__in=(leaves + unplanned_tour_plan)
        )
        tour_plan_list = [i.tour_plan.tour_plan.id for i in get_month_mpo_tour_plan]
        company_area_tour_plan = [i.company_mpo_area_id.id for i in CompanyMPOAreaTourPlan.objects.filter(
            tour_plan_id__in=tour_plan_list)]
        # company_area_tour_plan = [i.tour_plan.tour_plan.select_the_area.id for i in get_month_mpo_tour_plan]
        doctor_list_tour_plan = CompanyWiseDoctor.objects.filter(
            company_name__company_id=company,
            doctor_name__doctor_territory__id__in=company_area_tour_plan
        )
        doctor_dcr_list_for_month = [i.dcr.dcr.visited_doctor for i in MpoWiseShiftwiseDcrForDoctor.objects.filter(
            dcr__dcr__month=request.data.get('month'),
            dcr__dcr__year=request.data.get('year')
        )]
        chemist_list_tour_plan = CompanyWiseChemist.objects.filter(
            company_name__company_id=company,
            chemist_name__chemist_territory__in=company_area_tour_plan
        )
        chemist_dcr_list_for_month = [i.dcr.dcr.visited_chemist for i in MpoWiseShiftwiseDcrForChemist.objects.filter(
            dcr__dcr__month=request.data.get('month'),
            dcr__dcr__year=request.data.get('year')
        )]
        missed_doctors = list(set(doctor_list_tour_plan) - set(doctor_dcr_list_for_month))
        missed_chemist = list(set(chemist_list_tour_plan) - set(chemist_dcr_list_for_month))
        missed_doctors_object = [
            MPOMissedCallModel(
                mpo_name=i,
                company_name=Company.objects.get(company_id=company),
                doctor=doctor_name,
                year=year,
                month=month) for doctor_name in missed_doctors]
        missed_chemist_object = [
            MPOMissedCallModel(
                mpo_name=i,
                company_name=Company.objects.get(company_id=company),
                chemist=chemist_name,
                year=year,
                month=month
            ) for chemist_name in missed_chemist
        ]
        all_data = missed_chemist_object + missed_doctors_object
        MPOMissedCallModel.objects.bulk_create(all_data)
        
        CompanyMpoTourPlan.objects.filter(
            mpo_name__id=i.id,
            tour_plan__tour_plan__select_the_month=month,
            tour_plan__tour_plan__select_the_date_id__year=year).update(
                is_missed_call_calculated=True)
         
    return Response(
        {'Sucessfully created'},
        status=status.HTTP_201_CREATED)


@api_view(['POST'])
def get_mpo_data(request):
    mpo = request.data.get('mpo')
    month = request.data.get('month')
    year = request.data.get('year')
    date_dict = get_nepali_dates_for_month(year, month)
    return_data = []
    for date in date_dict.keys():
        doctor_dcr = MpoWiseShiftwiseDcrForDoctor.objects.filter(
            mpo_name__id=mpo,
            dcr__dcr__date=date
        )
        chemist_dcr = MpoWiseShiftwiseDcrForChemist.objects.filter(
            mpo_name__id=mpo,
            dcr__dcr__date=date
        )
        stockist_dcr = MpoWiseShiftwiseDcrForStockist.objects.filter(
            mpo_name__id=mpo,
            dcr__dcr__date=date
        )
        total_joined_call = (DcrForStockistCompanyRolesMap.objects.filter(
            dcr_id__in=stockist_dcr.values_list('id', flat=True)
        ).count() + DcrForChemistCompanyRolesMap.objects.filter(
            dcr_id__in=chemist_dcr.values_list('id', flat=True)
        ).count() + DcrForDoctorCompanyRolesMap.objects.filter(
            dcr_id__in=doctor_dcr.values_list('id', flat=True)
        ).count())
        return_data.append(
            {
            'date': date,
            'doctor_call': doctor_dcr.count(),
            'chemist_call': chemist_dcr.count(),
            'stockist_call': stockist_dcr.count(),
            'total_joined_call': total_joined_call}
        )
    return Response(data=return_data)


@api_view(['POST'])
def get_higher_order_data(request):
    user = request.data.get('user')
    month = request.data.get('month')
    year = request.data.get('year')
    date_dict = get_nepali_dates_for_month(year, month)
    return_data = []
    for date in date_dict.keys():
        dcr = HigherOrderDCR.objects.filter(
            user_id__id=user,
            date=date
        ).count()
        return_data.append(
            {
            'date': date,
            'call_data': dcr
            }
        )
    return Response(data=return_data)


