from DCRUser.logic import get_user_from_access

def product_data_transmission(request):
    add_update_data = {
    'company_name':request.data.get('company_id'),
    'product_name':{
        'product_name': request.data.get('product_name'),
        'product_molecular_name': request.data.get(
        'product_molecular_name'),
        'product_price_per_strip_in_mrp': request.data.get(
            'product_price_per_strip_in_mrp'),
        'product_price_for_stockist': request.data.get(
            'product_price_for_stockist'
        ),
        'product_description': request.data.get(
        'product_description'
        ),
        'product_image': request.data.get(
        'product_image'
        )
    },
    'division_name':request.data.get('division_name'),
    'product_type': request.data.get('product_type'),
    'bonus': request.data.get('bnous')
    }
    return add_update_data