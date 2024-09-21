import calendar
from Doctors.utils import get_user_from_access
from django.db.models import Count, Max
from Company.models import CompanyRoles
from datetime import datetime, timedelta
from Mpo.models import ActiveWorkingDays, CompanyMpoTourPlan
from DCRUser.models import (CompanyUserRole,
                            CompanyUser)
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync
from chat.models import GeneralNotification, GroupMembers
from DCRUser.models import User
from chat.consumers import ChatAsyncConsumer
from dailycallrecord.utils import nepali_month_from_english
from .exceptions import GroupNameError


def get_maximum_priority_role(company_name):
    max_quantity = CompanyRoles.objects.filter(company_name=company_name).aggregate(Max('priority_value'))['priority_value__max']
    item = CompanyRoles.objects.filter(priority_value=max_quantity).first()
    output = { 
    'priority_value' : max_quantity,
    'role_name' : item.role_name.role_name,
    'role_id' : item.role_name.role_id
    }
    return output


def get_role_priority_value(role_id, company_name):
    instance = CompanyRoles.objects.get(company_name=company_name,role_name=role_id)
    return instance.priority_value


def get_year_month_from_date(selected_date):
    date_object = datetime.strptime(selected_date, "%Y-%m-%d")
    month = date_object.strftime("%B")
    month = nepali_month_from_english(month)
    year = date_object.strftime("%Y")
    data = {'month':month, 'year':year}
    return data


def mpo_data_transmission(request):
    # company_name = request.data.get('company_name')
    # dates = request.data[0].get('dates')
    approved_by = request.data[0].get('approved_by')
    # year_month = get_year_month_from_date(dates[0])
    # instance = CompanyUserRole.objects.get(id=request.data.get('mpo_name'))
    create_data = {
        # 'dates':dates,
        'mpo_name':request.data[0].get('mpo_name'),
        'company_name':request.data[0].get('company_name'),
        'tour_plan':{
            'shift':
                {'shift':request.data[0].get('shift'),
                },
            'tour_plan':
            {
            # 'select_the_month':year_month['month'],
            'select_the_month':request.data[0].get('month'),
            'select_the_date_id':request.data[0].get('select_the_date'),
            'select_the_area':request.data[0].get('select_the_area'),
            'purpose_of_visit':request.data[0].get('purpose_of_visit'),
            'is_dcr_added':request.data[0].get('is_dcr_added'),
            'is_unplanned':request.data[0].get('is_unplanned'),
            'hulting_station': request.data[0].get('hulting_station')
        }
        },
        'approved_by':approved_by,
        'is_approved':request.data[0].get('is_approved'),
        # 'submit_to':instance.executive_level.id
    }
    sending_data = []
    for date in create_data['dates']:
        sending_data.append({
        'mpo_name':request.data.get('mpo_name'),
        'company_name':request.data.get('company_name'),
        'tour_plan':{
            'shift':
                {'shift':request.data.get('shift'),
                },
            'tour_plan':
            {
            'select_the_month':request.data.get('month'),
            # 'select_the_month':year_month['month'],
            'select_the_date_id':date,
            'select_the_area':request.data.get('select_the_area'),
            'purpose_of_visit':request.data.get('purpose_of_visit'),
            'is_dcr_added':request.data.get('is_dcr_added'),
            'is_unplanned':request.data.get('is_unplanned'),
            'hulting_station': request.data.get('hulting_station')
        }
        },
        'approved_by':approved_by,
        'is_approved':request.data.get('is_approved'),
        # 'submit_to':instance.executive_level.id
    })
    return sending_data


def get_upper_level_user_id(company_user_role_id):
    if CompanyUserRole.objects.filter(id=company_user_role_id).exists():
        company_user_role_instance = CompanyUserRole.objects.get(
            id=company_user_role_id)
        if company_user_role_instance.executive_level:
            company_user_instance = CompanyUser.objects.get(
                id=company_user_role_instance.executive_level.id
            )
            return company_user_instance.user_name.id
        else:
            return None
    else:
        return None


def get_user_id(company_user_role_id):
    if CompanyUserRole.objects.filter(id=company_user_role_id).exists():
        company_user_role_instance = CompanyUserRole.objects.get(
            id=company_user_role_id
        )
        return company_user_role_instance.user_name.id
    else:
        return None


def get_user_name(company_user_role_id):
    if CompanyUserRole.objects.filter(id=company_user_role_id).exists():
        company_user_role_instance = CompanyUserRole.objects.get(
            id=company_user_role_id
        )
        return (company_user_role_instance.user_name.first_name
                + ' '+ company_user_role_instance.user_name.last_name)
    else:
        return None
    

def mpo_update_data_transmission(request):
    month = ''
    year = ''
    if request.data.get('select_the_date'):
        year_month = get_year_month_from_date(request.data.get('select_the_date'))
        month = year_month['month']
        year = year_month['year']
    if request.data.get('approved_by'):
        instance = CompanyUserRole.objects.get(id=request.data.get('approved_by'))
        # submit_to_instance = CompanyUserRole.objects.get(user_name=instance.executive_level.user_name.id)
        create_data = {
            'mpo_name':request.data.get('mpo_name'),
            'company_name':request.data.get('company_name'),
            'tour_plan':{
                'shift':
                {'shift':request.data.get('shift'),
                },
                'tour_plan':
                {
                'select_the_month':month,
                'select_the_date_id':request.data.get('select_the_date'),
                'purpose_of_visit':request.data.get('purpose_of_visit'),
                'is_dcr_added': request.data.get('is_dcr_added', False),
                'is_unplanned': request.data.get('is_unplanned', False),
                'is_admin_opened': request.data.get('is_admin_opened', False),
                'is_doctor_dcr_added': request.data.get('is_doctor_dcr_added', False),
                'is_chemist_dcr_added': request.data.get('is_chemist_dcr_added', False),
                'is_stockist_dcr_added': request.data.get('is_stockist_dcr_added', False),
                'hulting_station': request.data.get('hulting_station')
            }
            },
            'mpo_area': request.data.get('mpo_area'),
            'approved_by':request.data.get('approved_by'),
            'is_approved':request.data.get('is_approved'),
            # 'submit_to':instance.executive_level.id
        }
        return create_data
    else:
        create_data = {
            'mpo_name':request.data.get('mpo_name'),
            'company_name':request.data.get('company_name'),
            'tour_plan':{
                'shift':
                {'shift':request.data.get('shift'),
                },
                'tour_plan':
                {
                'select_the_month':month,
                'select_the_date_id':request.data.get('select_the_date'),
                'purpose_of_visit':request.data.get('purpose_of_visit'),
                'is_dcr_added': request.data.get('is_dcr_added', False),
                'is_unplanned': request.data.get('is_unplanned', False),
                'is_admin_opened': request.data.get('is_admin_opened', False),
                'is_doctor_dcr_added': request.data.get('is_doctor_dcr_added', False),
                'is_chemist_dcr_added': request.data.get('is_chemist_dcr_added', False),
                'is_stockist_dcr_added': request.data.get('is_stockist_dcr_added', False),
                'hulting_station': request.data.get('hulting_station')
            }
            },
            'mpo_area': request.data.get('mpo_area'),
            'approved_by':request.data.get('approved_by'),
            'is_approved':request.data.get('is_approved'),
            # 'submit_to':request.data.get('submit_to')
        }
        return create_data


def get_dates_x_years(n_years_ahead):
    start_date = datetime.now()
    end_date = start_date + timedelta(days=365*n_years_ahead)
    all_dates = []
    while start_date <= end_date:
        all_dates.append(start_date.strftime("%Y-%m-%d"))
        start_date += timedelta(days=1)
    return all_dates


def datetime_string(datetime_string):
    date_format = "%Y-%m-%dT%H:%M:%S"
    datetime_string = datetime_string[:19]
    date_object = datetime.strptime(datetime_string, date_format)
    return date_object


def tourplan_notification_send(data):
    channel_layer = get_channel_layer()
    if GroupMembers.objects.filter(user_id=data['receiver_id']).exists():
        group_name = GroupMembers.objects.get(user_id=data['receiver_id']).unique_id
    else:
        raise GroupNameError("The user id does not exist in our notification group!!!")
    GeneralNotification(
        general_notification_title=f"{data['type']} succesfully created",
        general_notification_description=f"{data['sender_name']} has succesfully {data['operation']} {data['type']}",
        general_notification_url = data["url"],
        general_notification_sender=User.objects.get(id=data['sender_id']),
        general_notification_receiver=User.objects.get(id=data['receiver_id'])).save()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'handle.message',  # Method name of the consumer
            'title':data['title'],
            'message': json.dumps({
                'default': False,
                'type': 'notifications',
                'message': f"{data['sender_name']} has succesfully {data['operation']} {data['type']}"}),  # Additional data to pass
        },
    )


def general_notification_send(data):
    channel_layer = get_channel_layer()
    if GroupMembers.objects.filter(user_id=data['receiver_id']).exists():
        group_name = GroupMembers.objects.get(user_id=data['receiver_id']).unique_id
    else:
        raise GroupNameError("The user id does not exist in our notification group!!!")
    GeneralNotification(
        general_notification_title=f"{data['notification_title']}",
        general_notification_description=f"{data['notification_description']}",
        general_notification_url = data["url"],
        general_notification_sender=User.objects.get(id=data['sender_id']),
        general_notification_receiver=User.objects.get(id=data['receiver_id'])).save()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'handle.message',  # Method name of the consumer
            'title':data['notification_title'],
            'message': json.dumps({
                'default': False,
                'type': 'notifications',
                'message': f"{data['notification_description']}"}),  # Additional data to pass
        },
    )


def get_next_month(month_name):
    # Create a mapping of month names to month numbers
    month_mapping = {month.lower(): i for i, month in enumerate(calendar.month_name)}

    # Convert input month name to lowercase and get the corresponding month number
    current_month_number = month_mapping[month_name.lower()]

    # Calculate the next month number
    next_month_number = (current_month_number % 12) + 1

    # Get the name of the next month
    next_month_name = calendar.month_name[next_month_number]

    return next_month_name


def get_next_month_date(current_date):
    # Calculate the first day of the next month
    next_month = current_date.replace(day=1) + timedelta(days=32)

    # If the next month is in the next year, adjust the year
    if next_month.year > current_date.year:
        next_month = next_month.replace(year=current_date.year + 1)

    # Calculate the next month's date with the same day
    try:
        next_month_date = next_month.replace(day=current_date.day)
    except ValueError:
        # If the day is not valid in the next month (e.g., January 31st),
        # return None
        return None
    return next_month_date


def get_unplanned_tour_plan_dates_month(year, month, mpo):
    mpo_tour_plan = CompanyMpoTourPlan.objects.filter(
        tour_plan__tour_plan__select_the_month=month,
        tour_plan__tour_plan__select_the_date_id__year=year,
        mpo_name__id=mpo,
        tour_plan__tour_plan__is_unplanned=True
    )
    return [i.tour_plan.select_the_date_id for i in mpo_tour_plan]
