from DCRUser.logic import get_user_from_access

def stockist_data_transmission(request):
    add_update_data = {
        'stockist_name':{
            'stockist_category': request.data.get('stockist_category'),
            'stockist_name': request.data.get('stockist_name'),
            'stockist_address': request.data.get('stockist_address'),
            'stockist_contact_number': request.data.get('stockist_contact_number'),
            'stockist_territory': request.data.get('stockist_territory'),
            'pan_vat_number': request.data.get('pan_vat_number')
        },
        'company_name':request.data.get('company_name')
    }
    return add_update_data