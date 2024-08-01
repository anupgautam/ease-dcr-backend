from DCRUser.logic import get_user_from_access
from Company.models import Company

def chemsit_data_transmission(request):
    create_update_data = {
        'chemist_category': request.data.get('chemist_category'),
        'chemist_name': request.data.get('chemist_name'),
        'chemist_address': request.data.get('chemist_address'),
        'chemist_gender': request.data.get('chemist_gender'),
        'chemist_phone_number': request.data.get('chemist_phone_number'),
        'chemist_territory':request.data.get('chemist_territory'),
        'company_name': request.data.get('company_id'),
        'chemist_contact_person':request.data.get('chemist_contact_person'),
        'chemist_pan_number':request.data.get("chemist_pan_number"),
        'mpo_name': request.data.get('mpo_name'),
        'is_investment': request.data.get('is_investment')
    }
    return create_update_data

def chemist_category_data(request):
    create_update_data = {
        'category_name':{
        'category_name':request.data.get('category_name'),
        },
        'company_name':request.data.get('company_name')
    }
    return create_update_data