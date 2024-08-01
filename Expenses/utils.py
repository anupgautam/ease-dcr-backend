from abc import ABC, abstractmethod
from datetime import datetime, timedelta, date
import calendar

from django.utils import timezone
from django.db.models import Q
from django.apps import apps

from Expenses.models import CompanyAreaWiseExpeneses, LeaveApplication, MpoWiseLeaveApplication
from DCRUser.models import CompanyUserRole
from dailycallrecord.models import (MpoWiseShiftwiseDcrForChemist,
                                    MpoWiseShiftwiseDcrForDoctor,
                                    MpoWiseShiftwiseDcrForStockist)
from utility.dateUtils import DateUtilsWithDate
from Mpo.utils import (
    general_notification_send,
    get_user_id,
    get_user_name,
    get_upper_level_user_id
)

def get_expenses_according_to_area_and_user():
    pass

def application_data(request):
    is_approved = False
    if request.data.get('is_approved'):
        is_approved = request.data.get('is_approved')
    data = {
        'mpo_name':request.data.get('mpo_name'),
        'application_id':{
            'leave_type':request.data.get('leave_type'),
            'leave_cause':request.data.get('leave_cause'),
            'leave_from':request.data.get('leave_from'),
            'leave_to':request.data.get('leave_to'),
            'company_name':request.data.get('company_name'),
            'leave_status':request.data.get('leave_status'),
            'is_submitted':request.data.get('is_submitted'),
            'is_approved':is_approved
            # 'submit_to':request.data.get('submit_to')
        }
    }
    return data

def get_company(company_user_role_id):
    company_user_role_instance = CompanyUserRole.objects.get(
        id=company_user_role_id
    )
    return company_user_role_instance.company_name.company_id

def get_admin_user_id(company_id):
    company_user_role_instance = CompanyUserRole.objects.get(
            company_name__company_id=company_id,
            role_name__role_name__role_name='admin'
        )
    return company_user_role_instance.user_name.id

def application_notification_send(mpo_name, add, status, leave_from, leave_to):
    if add ==  True:
        general_notification_send(
                {
                    'type':"Application",
                    "receiver_id":get_admin_user_id(get_company(mpo_name)),
                    "sender_name":get_user_name(mpo_name),
                    "url":"",
                    "sender_id":get_user_id(mpo_name),
                    "notification_title":"Application Created",
                    "notification_description":f"{get_user_name(mpo_name)} has issued an leave application from {leave_from} to {leave_to}"
                }
            )
    else:
        general_notification_send(
                {
                    'type':"Application",
                    "receiver_id":get_user_id(mpo_name),
                    "sender_name":"Admin",
                    "url":"",
                    "sender_id":get_admin_user_id(get_company(mpo_name)),
                    "notification_title":"Application Created",
                    "notification_description":f"Admin has {status} your application leave from {leave_from} to {leave_to}"
                }
            )


def target_data(request):
    data = {
        'year':request.data.get('year'),
        'target_from':request.data.get('target_from'),
        'target_to':request.data.get('target_to'),
        'target_amount':request.data.get('target_amount'),
        'sales':request.data.get('sales'),
    }
    return data

def upload_data(request):
    data = {
        'mpo_name':request.data.get('mpo_name'),
        'upload_type':request.data.get('upload_type'),
        'upload':request.data.get('upload'),
        'upload_name':request.data.get('upload_name')
    }
    return data


FIRST_QUATER_MONTH = ["January", "February", "March",]
SECOND_QUATER_MONTH = ["April", "May", "June",]
THIRD_QUATER_MONTH = ["July", "August", "September",]
FOURTH_QUATER_MONTH = ["October", "November", "December",]

APP_NAME = "dailycallrecord"

class DailyCallRecordInstances():

    def __init__(self, model_name, app_name, mpo_name, month=None, year=None) -> None:
        self.model_name = model_name
        self.app_name = app_name
        self.mpo_name = mpo_name
        self.date_utils = DateUtilsWithDate
        self.month = month
        self.year = year

    def get_instances_according_to_date(self):
        instance = apps.get_model(self.app_name,
                                  self.model_name
                                  ).objects.filter(
                                    dcr__dcr__date="2010-01-10")
        return instance
    
    def get_instances_according_to_the_week(self):
            instance = apps.get_model(self.app_name, self.model_name).objects.filter(
                Q(mpo_name=self.mpo_name) &
                Q(dcr__dcr__date__range=(
                    self.date_utils().get_first_date_of_the_week(),
                    self.date_utils().get_last_date_of_the_week())))
            return instance

    def get_instance_according_to_the_month_and_year(self):
        instance = apps.get_model(self.app_name, self.model_name).objects.filter(
            mpo_name = self.mpo_name,
            dcr__dcr__month=self.month,
            dcr__dcr__year=self.year
        )
        return instance
    
    def get_instance_according_to_the_year(self):
        instance = apps.get_model(self.app_name, self.model_name).objects.filter(
            mpo_name=self.mpo_name,
            dcr__dcr__year=self.year
        )
        return instance
    
    def get_model_name(self):
        return self.model_name
    
    def get_app_name(self):
        return self.app_name
    

class MiscellaneousExpenses():

    def __init__(self, mpo_name, model_list, app_name, quarter=None, month=None, year=None) -> None:
        self.mpo_name = mpo_name
        self.dcr_instance = DailyCallRecordInstances
        self.model_list = model_list
        self.app_name = app_name
        self.month = month
        self.year = year
        self.quarter = quarter
    
    def get_expenses(self, instance_list):
        expenses = 0
        for i in instance_list:
            if i.dcr.dcr.expenses:
                expenses+=(i.dcr.dcr.expenses)
        return expenses

    def daily_miscellaneous_expenses(self, model_name,app_name):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
        ).get_instances_according_to_date()
        return self.get_expenses(instance)

    def get_daily_miscellaneous_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.daily_miscellaneous_expenses(i, self.app_name)
        return total
    
    def weekly_miscellaneous_expenses(self, model_name, app_name):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name).get_instances_according_to_the_week()
        return self.get_expenses(instance)  
    
    def get_weekly_miscellaneous_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.weekly_miscellaneous_expenses(i, self.app_name)
        return total
    
    def monthly_miscellaneous_expenses(self, app_name, model_name, month, year):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
            year=year,
            month=month
        ).get_instance_according_to_the_month_and_year()
        return self.get_expenses(instance)
    
    def get_monthly_miscellaneous_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.monthly_miscellaneous_expenses(self.app_name, i, self.month, self.year)
        return total

    def quarterly_miscellaneous_expenses(self, model_name, app_name, month, year):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
            year=year,
            month=month
        ).get_instance_according_to_the_month_and_year()
        return self.get_expenses(instance)
    
    def get_quarterly_miscellaneous_expenses(self):
        total = 0
        if self.quarter==1:
            for i in FIRST_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_miscellaneous_expenses(
                        j, self.app_name, i, self.year)
        if self.quarter==2:
            for i in SECOND_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_miscellaneous_expenses(
                        j, self.app_name, i, self.year)
        if self.quarter==3:
            for i in THIRD_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_miscellaneous_expenses(
                        j, self.app_name, i, self.year)
        if self.quarter==4:
            for i in FOURTH_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_miscellaneous_expenses(
                        j, self.app_name, i, self.year)
        return total
    
    def yearly_miscellaneous_expenses(self, app_name, model_name,year):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
            year=year
        ).get_instance_according_to_the_year()
        return self.get_expenses(instance)
    
    def get_yearly_miscellaneous_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.yearly_miscellaneous_expenses(
                self.app_name, i, self.year)
        return total


class Expenses():
    def __init__(self, company_name, model_list, app_name, mpo_name, month=None, year=None, quarter=None) -> None:
        self.model_list = model_list
        self.app_name = app_name
        self.company_name = company_name
        self.dcr_instance = DailyCallRecordInstances
        self.mpo_name =mpo_name
        self.date_utils = DateUtilsWithDate
        self.month = month
        self.year = year
        self.quarter = quarter
    
    def get_expenses_according_to_area(self,area_name):
        instance = CompanyAreaWiseExpeneses.objects.get(
            id=area_name)
        return instance.expenses_rate

    def expenses_according_to_area(self,instance_list):
        total = 0
        for i in instance_list:
            total += self.get_expenses_according_to_area(
                i.dcr.dcr.visited_area.id)
        return total
    
    def daily_expenses(self, model_name, app_name):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
        ).get_instances_according_to_date()
        return self.expenses_according_to_area(instance)
    
    def get_daily_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.daily_expenses(i, self.app_name)
        return total
    
    def weekly_expenses(self,model_name,app_name):
        instance = self.dcr_instance(
        model_name=model_name,
        app_name=app_name,
        mpo_name=self.mpo_name).get_instances_according_to_the_week()
        return self.expenses_according_to_area(instance)
    
    def get_weekly_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.weekly_expenses(i, self.app_name)
        return total
    
    def monthly_expenses(self, app_name, model_name, month, year):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
            year=year,
            month=month
        ).get_instance_according_to_the_month_and_year()
        return self.expenses_according_to_area(instance)
    
    def get_monthly_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.monthly_expenses(self.app_name, i, self.month, self.year)
        return total
    
    def quarterly_expenses(self, model_name, app_name, month, year):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
            year=year,
            month=month
        ).get_instance_according_to_the_month_and_year()
        return self.expenses_according_to_area(instance)
    
    def get_quarterly_expenses(self):
        total = 0
        if self.quarter==1:
            for i in FIRST_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_expenses(
                        j, self.app_name, i, self.year)
        if self.quarter==2:
            for i in SECOND_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_expenses(
                        j, self.app_name, i, self.year)
        if self.quarter==3:
            for i in THIRD_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_expenses(
                        j, self.app_name, i, self.year)
        if self.quarter==4:
            for i in FOURTH_QUATER_MONTH:
                for j in self.model_list:
                    total +=self.quarterly_expenses(
                        j, self.app_name, i, self.year)
        return total
    
    def yearly_expenses(self, app_name, model_name,year):
        instance = self.dcr_instance(
            model_name=model_name,
            app_name=app_name,
            mpo_name=self.mpo_name,
            year=year
        ).get_instance_according_to_the_year()
        return self.expenses_according_to_area(instance)
    
    def get_yearly_expenses(self):
        total = 0
        for i in self.model_list:
            total += self.yearly_expenses(
                self.app_name, i, self.year)
        return total
    

class DetailedExpenses(Expenses, MiscellaneousExpenses):
    def __init__(self, company_name, model_list, app_name, mpo_name, month=None, year=None,) -> None:
        self.model_list = model_list
        self.app_name = app_name
        self.company_name = company_name
        self.dcr_instance = DailyCallRecordInstances
        self.mpo_name =mpo_name
        self.date_utils = DateUtilsWithDate
        self.month = month
        self.year = year
    
    def get_single_miscellaneous_expenses(self, instance):
        return instance.dcr.dcr.expenses
    
    def monthly_date_and_expenses(self, app_name, model_name, month, year):
        instance = self.dcr_instance(
        model_name=model_name,
        app_name=app_name,
        mpo_name=self.mpo_name,
        year=year,
        month=month
        ).get_instance_according_to_the_month_and_year()
        return instance

    def detailed_expenses(self):
        detailed_list = []
        for i in self.model_list:
            instance = self.monthly_date_and_expenses(self.app_name, i,self.month, self.year)
            for j in instance:
                detailed_list.append({'date':j.dcr.dcr.date,
                                      'area_expenses':self.get_expenses_according_to_area(j.dcr.dcr.visited_area.id),
                                      'miscellaneous_expenses':self.get_single_miscellaneous_expenses(j),
                                      'shift':j.dcr.shift.shift})
        return detailed_list
    

month_name_to_number = {
    'Baisakh': 1,
    'Jestha': 2,
    'Ashad': 3,
    'Shrawan': 4,
    'Bhadra': 5,
    'Asoj': 6,
    'Kartik': 7,
    'Mangsir': 8,
    "Poush": 9,
    "Magh": 10,
    'Falgun': 11,
    'Chaitra': 12}

def get_all_leave_dates_from_month(year, month, mpo_name):
    month_number = month_name_to_number.get(month)
    # Check if the month is valid
    if month_number:
        # Get the first day of the specified month
        start_date = datetime(
            year=int(year),
            month=int(month_number),
            day=1).date()

        # Get the last day of the specified month
        end_date = datetime(year=int(year), month=int(month_number), day=30).date()

        mpo_leave_applications_id = [
            i.application_id.id for i in MpoWiseLeaveApplication.objects.filter(
                mpo_name__id=mpo_name)]

        # Query to get all LeaveApplications for the specified month
        leave_applications = LeaveApplication.objects.filter(
            leave_from__gte=start_date,
            leave_to__lte=end_date,
            id__in=mpo_leave_applications_id
        )

        # Extract leave dates from each LeaveApplication instance
        leave_dates = []
        for leave_application in leave_applications:
            current_date = leave_application.leave_from
            while current_date <= leave_application.leave_to:
                leave_dates.append(current_date)
                current_date += timedelta(days=1)
        return leave_dates

        # Now leave_dates contains a list of all leave dates within the specified month
    else:
        pass