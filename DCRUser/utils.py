def company_user_data_transmission(email, request):
    # company_name = request.data.get('company_id')
    # role_id = CompanyRoles.objects.get(id=request.data.get('role_name'),company_name=request.data.get('company_id')).role_name.role_id
    create_and_update_data = {
        "user_name": {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "middle_name": request.data.get("middle_name"),
            "email": email,
            "phone_number": request.data.get("phone_number"),
            "address": request.data.get("address"),
            "date_of_joining": request.data.get("date_of_joining"),
            "is_active": request.data.get("is_active"),
            "password": 12345,
            "confirm_password": 12345,
        },
        "company_name": request.data.get("company_id"),
        # 'role_name':{
        #     'id': request.data.get('role_name'),
        #     'role_name': CompanyRoles.objects.get(id=request.data.get('role_name'),
        #                                           company_name=company_name).role_name.role_id,
        #     'company_name':request.data.get('company_id'),
        #     'priority_value':get_role_priority_value(role_id, company_name)
        # },
        "role_name": request.data.get("role_name"),
        # 'division_name':CompanyWiseDivision.objects.get(id=request.data.get('division_name'), company_name=company_name).division_name.id
        "division_name": request.data.get("division_name"),
        "executive_level": request.data.get("executive_level"),
        "company_area": request.data.get("company_area"),
        "station_type": request.data.get("station_type"),
    }

    return create_and_update_data


month_number_to_name = {
    1: "Baisakh",
    2: "Jestha",
    3: "Asadh",
    4: "Shrawan",
    5: "Bhadra",
    6: "Asoj",
    7: "Kartik",
    8: "Mangsir",
    9: "Poush",
    10: "Magh",
    11: "Falgun",
    12: "Chaitra",
}
