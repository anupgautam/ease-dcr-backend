from DCRUser.models import CompanyUserRole


def get_company_id_from_company_user_role(id):
    instance = CompanyUserRole.objects.get(id=id)
    return instance.company_name.company_id