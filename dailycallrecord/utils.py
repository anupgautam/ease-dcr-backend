from datetime import datetime
# This function is used to transfer the data 
# for creating and updating the dcr of the doctor

def dcr_for_doctor_data_transmission(request):
    create_update_data = {
        'mpo_name' : request.data.get('mpo_name'),
        'dcr':{
            'shift': request.data.get('shift'),
            'dcr': request.data.get('dcr_id')
        }
    }
        # {
        # 'mpo_name' :1,
        # 'dcr':{
        #     'shift': 2,
        #     'dcr':{
        #         'visited_doctor': request.data.get('visited_doctor'),
        #         'promoted_product': request.data.get('promoted_product'),
        #         'visited_with': request.data.get('visited_with'),
        #         'rewarded_with': request.data.get('rewarded_with'),
        #     }
        # }
    # },
    
    
    return create_update_data


# for chemist data transmission fro dcr
def dcr_for_chemist_data_transmission(request):
    create_update_data = {
        'mpo_name' : request.data.get('mpo_name'),
        'dcr':{
            'shift': request.data.get('shift'),
            'dcr': request.data.get('dcr_id')
        }
    }
    return create_update_data


# for stockist data transmission fro dcr
def dcr_for_stockist_data_transmission(request):
    create_update_data = {
        'mpo_name' : request.data.get('mpo_name'),
        'dcr':{
            'shift': request.data.get('shift'),
            'dcr': request.data.get('dcr_id')
        }
    }
    return create_update_data
def stockist_ordered_product_information(request):
    create_update_data = {
            'dcr_id':request.data.get('dcr_id'),
            'ordered_product':{
                'ordered_product':request.data.get('product_id'),
                'ordered_quantity':request.data.get('ordered_quantity')
            }
        }
    return create_update_data

def nepali_month_from_english(english_month):
    mapping_data = {
        'January': 'Baisakh',
        'February': 'Jestha',
        'March': 'Asadh',
        'April': 'Shrawan',
        'May': 'Bhadra',
        'June': 'Ashoj',
        'July': 'Kartik',
        'August': 'Mangsir',
        'September': 'Poush',
        'October': 'Magh',
        'November': 'Falgun',
        'December': 'Chaitra'}
    return mapping_data[english_month]

def nepali_month_to_digit(nepali_month):
    mapping_data = {
        'Baisakh': 1,
        'Jestha': 2,
        'Asadh': 3,
        'Shrawan': 4,
        'Bhadra': 5,
        'Ashoj': 6,
        'Kartik': 7,
        'Mangsir': 8,
        'Poush': 9,
        'Magh': 10,
        'Falgun': 11,
        'Chaitra': 12
    }
    return mapping_data[nepali_month]
