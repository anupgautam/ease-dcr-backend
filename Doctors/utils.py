from DCRUser.logic import get_user_from_access

def doctor_data_transmission(request):
    create_update_data = {
        'doctor_name': request.data.get('doctor_name'),
        'doctor_address': request.data.get('doctor_address'),
        'doctor_gender': request.data.get('doctor_gender'),
        'doctor_phone_number': request.data.get('doctor_phone_number'),
        'doctor_category': request.data.get('doctor_category'),
        'company_name': request.data.get('company_id'),
        'doctor_territory':request.data.get('doctor_territory'),
        'doctor_specialization':request.data.get('doctor_specialization'),
        'doctor_nmc_number':request.data.get('doctor_nmc_number'),
        'doctor_qualification':request.data.get('doctor_qualification'),
        'mpo_name': request.data.get('mpo_name'),
        'is_investment': request.data.get('is_investment')
    }
    return create_update_data

def doctor_category_data(request):
    create_update_data = {
        'category_name':{
        'category_name':request.data.get('category_name'),
        },
        'company_name':request.data.get('company_name')
    }
    return create_update_data