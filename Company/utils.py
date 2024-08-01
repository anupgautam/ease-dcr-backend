from Doctors.utils import get_user_from_access
from DCRUser.models import CompanyUserRole
from DCRUser.models import User
from Company.models import CompanySalaryRoles


def company_role_salary_data_transmission(request, company_name):
        crud_data ={
            'company_name':company_name,
            'company_roles':request.data.get('company_roles'),
            'salary':request.data.get('salary')
        }
        return crud_data


def company_area_crud_data_transmission(request):
    data = {
            'company_name': request.data.get('company_id'),
            'company_area': {
                'latitude':request.data.get('latitude'),
                'longitude':request.data.get('longitude'),
                'country':request.data.get('country'),
                'state':request.data.get('state'),
                'division':request.data.get('division'),
                'area_name':request.data.get('area_name')
            },
            'station_type': request.data.get('station_type')
        }
    return data


def company_division_crud_data_transmission(request):
      data = {
            'company_name':request.data.get('company_id'),
            'division_name':{
                  'division':request.data.get('division')
            }
      }
      return data
# def get_the_expenes_and_salary():
#     email = "add221@gmail.com"
#     user_id = User.objects.get(email=email)
#     company_name = 1
#     user = CompanyUserRole.objects.get(company_name=company_name,user_name=user_id.id)
#     role_name = user.role_name
#     
#     
#     company_role_wise_expenses = CompanyRoleWiseExpenses.objects.get(company_name=company_name,role_name=1)
#     
#     