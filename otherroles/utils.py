from DCRUser.models import CompanyUserRole,CompanyUser, User
from datetime import datetime
from dailycallrecord.utils import nepali_month_from_english
from utility.get_company_id_from_company_user_role import get_company_id_from_company_user_role
from bsdate.convertor import BSDateConverter

def data_transmission(request):
    obj = BSDateConverter()
    approved_by = ''
    if request.data.get('approved_by'):
        approved_by=request.data.get('approved_by')
    else:
        approved_by=None
    is_unplanned = False
    if request.data.get('is_unplanned'):
        is_unplanned=request.data.get('is_unplanned')
    company_user_role_instance = CompanyUserRole.objects.get(
        id=request.data.get('user_id'))
    sending_data = []
    dates = request.data.get('dates')
    for date in dates:
        new_date = obj.convert_bs_to_ad(date)
        month_year = datetime.strptime(new_date,"%Y-%m-%d")
        sending_data.append({
        # 'visited_with':{
        # },
        # 'company_id':{
            'company_id':get_company_id_from_company_user_role(request.data.get('user_id')),
        # },
        # 'user_id':{
            'user_id':request.data.get('user_id'),
        # },
        'approved_by':approved_by,
        # 'submit_to':company_user_role_instance.executive_level.id,
        'is_approved':False,
        # 'shift':{
            'shift':request.data.get('shift'),
        # },
        'date': new_date,
        'year':month_year.year,
        'month': nepali_month_from_english(month_year.strftime("%B")),
        'is_unplanned':is_unplanned,
        'hulting_station': request.data.get('hulting_station'),
        'visit_data': request.data.get('visit_data')
        })
    return sending_data

def update_data_transmission(request):
    obj = BSDateConverter()
    is_unplanned = False
    if request.data.get('is_unplanned'):
        is_unplanned=request.data.get('is_unplanned')
    approved_by = request.data.get('approved_by')
    if approved_by:
        approved_by=approved_by
    else:
        approved_by=None
    is_approved = request.data.get('is_approved')
    if is_approved:
        is_approved = is_approved
    else:
        is_approved = False
    date = obj.convert_bs_to_ad(request.data.get('date'))
    data ={
        # 'visited_with':{
            'visited_with':request.data.get('visited_with'),
        # },
        # 'company_id':{
        # 'company_id':get_company_id_from_company_user_role(request.data.get('user_id')),
            'company_id':request.data.get('company_id'),
        # },
        # 'user_id':{
            'user_id':request.data.get('user_id'),
        # },
        'approved_by':approved_by,
        'is_approved':is_approved,
        # 'shift':{
            'shift':request.data.get('shift'),
        # },
        'date': date,
        'is_unplanned':is_unplanned,
        'is_dcr_added':request.data.get('is_dcr_added'),
        'month': request.data.get('month'),
        'hulting_station': request.data.get('hulting_station'),
        'mpo_area': request.data.get('mpo_area')
    }
    return data

def dcr_data_transmission(request):
    obj = BSDateConverter()
    ad_date = obj.convert_bs_to_ad(request.data.get('date'))
    month_year = datetime.strptime(ad_date,"%Y-%m-%d")
    month = month_year.strftime("%B")
    month = nepali_month_from_english(month)
    year = month_year.year
    data = {
        'date':obj.convert_bs_to_ad(request.data.get('date')),
        'month':month,
        'year':year,
        'company_id':request.data.get('company_id'),
        'user_id':request.data.get('user_id'),
        'visited_with':request.data.get('visited_with'),
        'shift':request.data.get('shift'),
    }
    return data