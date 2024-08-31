from rest_framework import viewsets
from rest_framework import status
from django.db.models import Sum
from datetime import datetime


from Expenses.serializers import *
from rest_framework.response import Response
from .utils import application_data, target_data, upload_data
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from DCRUser.models import (CompanyUser, CompanyUserRole)
from .utils import MiscellaneousExpenses, Expenses, DetailedExpenses
from .constant import MODELS, APP_NAME
from django.http import JsonResponse
from Account.pagination import CustomPagination
from Doctors.search import UserWiseTrigramSearch, TrigramSearch
from Account.pagination import paginate_json_response
from .utils import (application_notification_send,
                    get_total_saturdays)
from Mpo.utils import (get_user_id,
                       get_user_name,
                       get_upper_level_user_id,
                       general_notification_send)
from DCRUser.models import CompanyUserAttendance
from Company.models import CompanyHolidayDate


class ExpensesTypeViewset(viewsets.ModelViewSet):
    model = ExpensesType
    queryset = ExpensesType.objects.all()
    serializer_class = ExpensesTypeSerializers


class CompanyAreaWiseExpensesViewset(viewsets.ModelViewSet):
    model = CompanyAreaWiseExpeneses
    queryset = CompanyAreaWiseExpeneses.objects.all()
    pagination_class = CustomPagination
    serializer_class = CompanyAreaWiseExpensesSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area_name', 'company_name']
    def create(self, request, *args, **kwargs):
        # data = {
        #     "company_name":request.data.get('company_name'),
        #     "area_name":request.data.get('role_name'),
        #     "expenses_type":request.data.get('expenses_type'),
        #     "expenses_rate":request.data.get('expenses_rate')
        # }
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = CompanyAreaWiseExpeneses.objects.get(id=kwargs.get('pk'))
        serializer = self.serializer_class(instance,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveApplicationViewset(viewsets.ModelViewSet):
    model = LeaveApplication
    queryset = LeaveApplication.objects.all()
    serializer_class = LeaveApplicationSerializers


class MpoWiseLeaveApplicationViewset(viewsets.ModelViewSet):
    model = MpoWiseLeaveApplication
    queryset = MpoWiseLeaveApplication.objects.all()
    serializer_class = MpoWiseLeaveApplicationSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['mpo_name',
                        "application_id__company_name",
                        'application_id__submission_date']
    
    def create(self, request, *args, **kwargs):
        data = application_data(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            # application_notification_send(mpo_name=data['mpo_name'],
            #                               add=True,
            #                               status="pending",
            #                               leave_from=data['application_id']['leave_from'],
            #                               leave_to=data['application_id']['leave_to'])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        data = application_data(request)
        instance = MpoWiseLeaveApplication.objects.get(id=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            application_notification_send(mpo_name=data['mpo_name'],
                                          add=False,
                                          status=data['application_id']['leave_status'],
                                          leave_from=data['application_id']['leave_from'],
                                          leave_to=data['application_id']['leave_to'])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TargetViewset(viewsets.ModelViewSet):
    # pagination_class = CustomPagination
    queryset = Target.objects.all()
    serializer_class = TargetSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['target_from__id',
                        'target_to__id',
                        'year',
                        'target_to__role_name']

    def create(self, request, *args, **kwargs):
        data = target_data(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            # general_notification_send(
            #     {
            #         'type':"Target",
            #         "receiver_id":get_user_id(data['target_to']),
            #         "sender_name":get_user_name(data['target_from']),
            #         "url":"",
            #         "sender_id":get_user_id(data['target_from']),
            #         "notification_title":"Tourplan Created",
            #         "notification_description":f"{get_user_name(data['target_from'])} has set a Target for you"
            #     }
            # )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        instance = Target.objects.get(id=kwargs.get('pk'))
        data = target_data(request)
        serializer = self.serializer_class(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(detail=False, methods=['post'])
    def search_target(self, request, *args, **kwargs):
        search_data = TrigramSearch(request.data.get('search'),
                             'Target',
                             ['target_from__user_name__first_name',
                              'target_from__user_name__last_name',
                              'target_from__role_name__role_name__role_name',
                              'target_to__user_name__first_name',
                              'target_to__user_name__last_name',
                              'target_to__role_name__role_name__role_name',
                              ],
                              'Expenses'
                              )
        serializer = self.get_serializer(search_data.search(), many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response([])
            

class UploadsViewset(viewsets.ModelViewSet):
    queryset = Uploads.objects.exclude(mpo_name__user_name__is_active=False)
    serializer_class = UploadsSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields= ['mpo_name']
    def create(self, request, *args, **kwargs):
        data = upload_data(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def update(self, request, *args, **kwargs):
        instance = Uploads.objects.get(id=kwargs.get('pk'))
        data = upload_data(request)
        serializer = self.serializer_class(instance,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
    @action(detail=False, methods=['post'])
    def search_uploads(self, request, *args, **kwargs):
        search_data = UserWiseTrigramSearch(request.data.get('search'),
                             'Uploads',
                             ['upload_name',
                              'upload_type'],
                              'Expenses',
                              request.data.get('user_id')
                              )
        serializer = self.get_serializer(search_data.search(), many=True)
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response("Search data doesnot exists")


# {

# sick_leave:1,

# casual_leave:1,

# paid_leave:1,

# leave_without_paid:1,

# holiday:2,

# saturday: 4,

# [{

# attendance_date:date huna paro,

# leave_type: '',

# leave:true or false

# holiday: true or false,

# saturday: false or true,

# }]

# }
@api_view(['post'])
def get_attendance(request):
    month = request.data.get('month')
    month_value = request.data.get('month_value')
    year = request.data.get('year')
    user_id = request.data.get('user_id')
    company_name = CompanyUserRole.objects.get(
                    id=user_id).company_name.company_id
    # is_saturday = lambda d : True if d.weekday()==5 else False
    # print(is_saturday(datetime(2024,8,11)))
    # saturday_count = get_total_saturdays(month=month_value,
    #                                     year=year)
    attendance_data = CompanyUserAttendance.objects.filter(
                                user_id=user_id,
                                month=month_value,
                                attendance_date__year=year)
    attendance_serializer = MpoWiseLeaveApplicationSerializers(
        attendance_data,
        many=True
    )
    casual_leave_count = MpoWiseLeaveApplication.objects.filter(
                                mpo_name=user_id,
                                application_id__leave_type="casual_leave",
                                application_id__is_approved=True
                                ).count()
    sick_leave_count = MpoWiseLeaveApplication.objects.filter(
                                mpo_name=user_id,
                                application_id__leave_type="sick_leave",
                                application_id__is_approved=True
                                ).count()
    paid_leave_count = MpoWiseLeaveApplication.objects.filter(
                                mpo_name=user_id,
                                application_id__leave_type="paid_leave",
                                application_id__is_approved=True
                                ).count()
    leave_without_pay_count = MpoWiseLeaveApplication.objects.filter(
                                mpo_name=user_id,
                                application_id__leave_type="leave_without_paid",
                                application_id__is_approved=True
                                ).count()
    holiday_count = CompanyHolidayDate.objects.filter(
                                company_name=company_name,
                                holiday_date__month=month_value,
                                ).count()
    saturday_count = CompanyUserAttendance.objects.filter(
                                        user_id=user_id,
                                        month=month,
                                        attendance_date__year=year,
                                        is_saturday=True).count()
    data = {
        "sick_leave":sick_leave_count,
        "casual_leave":casual_leave_count,
        "paid_leave":paid_leave_count,
        "leave_without_pay_leave":leave_without_pay_count,
        "holiday_leave":holiday_count,
        "saturday":saturday_count,
        "attendance_data":attendance_serializer.data
    }
    return JsonResponse(data,
                        status=201,headers={
                                'content_type':'application/json'
                                }, safe=False)


@api_view(['post'])
def get_target_of_user(request):
    if(request.data.get('id') and request.data.get('year')):
        sending_data = {
        'sales':[],
        'target_amount':[],
    }
        target_instance = Target.objects.filter(
            target_to=request.data.get('id'),
            year=request.data.get('year'))
        if target_instance:
            for i in target_instance:
                sending_data['sales'].append(int(i.sales))
                sending_data['target_amount'].append(int(i.target_amount))

        return JsonResponse(sending_data,
                            status=201,headers={
                                'content_type':'application/json'
                            }, safe=False)
    else:
        sending_data = {
            'sales':[],
            'target_amount':[],
            'year':[]
        }
        target_instance = Target.objects.filter(target_to=request.data.get('id'))
        for i in target_instance:
            sending_data['sales'].append(int(i.sales))
            sending_data['target_amount'].append(int(i.target_amount))
            sending_data['year'].append(i.year)

        return JsonResponse(sending_data,
                                status=201,headers={
                                    'content_type':'application/json'
                                }, safe=False)


@api_view(['post'])
def expenses(request):
    expenses = Expenses(
        mpo_name=request.data.get('mpo_name'),
        model_list=MODELS,
        app_name=APP_NAME,
        company_name=request.data.get('company_name'),
        month=request.data.get('month'),
        year=request.data.get('year'),
        quarter=request.data.get('quarter')
    )
    miscellaneouos_expenses = MiscellaneousExpenses(
        mpo_name=request.data.get('mpo_name'),
        model_list=MODELS,
        app_name=APP_NAME,
        month=request.data.get('month'),
        year=request.data.get('year'),
        quarter=request.data.get('quarter')
    )
    data = {
        "daily":{
        'expenses':expenses.get_daily_expenses(),
        'miscellaneous_expenses':miscellaneouos_expenses.get_daily_miscellaneous_expenses()
        },
        "monthly":{
        'expenses':expenses.get_monthly_expenses(),
        'miscellaneous_expenses':miscellaneouos_expenses.get_monthly_miscellaneous_expenses() 
        },
        "quarterly":{
        'expenses':expenses.get_quarterly_expenses(),
        'miscellaneous_expenses':miscellaneouos_expenses.get_quarterly_miscellaneous_expenses()
        },
        "yearly":{
        'expenses':expenses.get_yearly_expenses(),
        'miscellaneous_expenses':miscellaneouos_expenses.get_yearly_miscellaneous_expenses()
        }
    }
    return JsonResponse(data,
                        status=201,headers={
                            'content_type':'application/json'
                        }, safe=False)


@api_view(['post'])
def get_whole_year_expenses(request):
    months = ["January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"]
    output = []
    for i in months:
        expenses = Expenses(
            mpo_name=request.data.get('mpo_name'),
            model_list=MODELS,
            app_name=APP_NAME,
            company_name=request.data.get('company_name'),
            month=i,
            year=request.data.get('year'),
            quarter=''
        )
        miscellaneouos_expenses = MiscellaneousExpenses(
            mpo_name=request.data.get('mpo_name'),
            model_list=MODELS,
            app_name=APP_NAME,
            month=i,
            year=request.data.get('year'),
            quarter=''
        )
        output.append(expenses.get_monthly_expenses() + miscellaneouos_expenses.get_monthly_miscellaneous_expenses())
    return JsonResponse(output,
                        status=201,headers={
                            'content_type':'application/json'
                        }, safe=False)


@api_view(['POST'])
@paginate_json_response()
def get_detailed_expenses(request):
    detailed_expenses = DetailedExpenses(mpo_name=request.data.get('mpo_name'),
                                         model_list=MODELS,
                                         app_name=APP_NAME,
                                         company_name=request.data.get('company_name'),
                                         month=request.data.get('month'),
                                         year=request.data.get('year'))
    response_data = {
        'results':detailed_expenses.detailed_expenses()
    }
    return JsonResponse(response_data,
                        status=200)


@api_view(['POST'])
def get_leave_user(request):
    if request.data.get('role_name'):
        mpo_leave_application_instance = MpoWiseLeaveApplication.objects.filter(
        application_id__is_approved=True,
            application_id__leave_from__lte=request.data.get('date'), 
            application_id__leave_to__gte=request.data.get('date'),
            mpo_name__role_name__id=request.data.get('role_name')
            )
        serializer = MpoWiseLeaveApplicationSerializers(
            mpo_leave_application_instance,
            many=True
        )
        return JsonResponse(serializer.data, safe=False)
    else:
        mpo_leave_application_instance = MpoWiseLeaveApplication.objects.filter(
            application_id__is_approved=True,
            application_id__leave_from__lte=request.data.get('date'), 
            application_id__leave_to__gte=request.data.get('date'))
        serializer = MpoWiseLeaveApplicationSerializers(
            mpo_leave_application_instance,
            many=True
        )
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def get_leave_user_according_to_role(request):
    mpo_leave_application_instance = MpoWiseLeaveApplication.objects.filter(
     application_id__is_approved=True,
        application_id__leave_from__lte=request.data.get('date'), 
        application_id__leave_to__gte=request.data.get('date'),
        mpo_name__role_name__id=request.data.get('role_name')
        )
    serializer = MpoWiseLeaveApplicationSerializers(
        mpo_leave_application_instance,
        many=True
    )
    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def get_leave_user_according_to_executive_level(request):
    user_instance = CompanyUserRole.objects.get(
        id=request.data.get('mpo_id')
    )
    company_user_instance = CompanyUser.objects.get(
        user_name=user_instance.user_name.id)
    if CompanyUserRole.objects.filter(
        executive_level=company_user_instance.id).exists():
        lower_executive_instances = CompanyUserRole.objects.filter(
            executive_level=company_user_instance.id
        )
        lower_order_ids = [i.id for i in lower_executive_instances]
        mpo_leave_application_instance = MpoWiseLeaveApplication.objects.filter(
        mpo_name__id__in=lower_order_ids,
        application_id__is_approved=True,
            application_id__leave_from__lte=request.data.get('date'), 
            application_id__leave_to__gte=request.data.get('date'),
            )
        serializer = MpoWiseLeaveApplicationSerializers(
            mpo_leave_application_instance,
            many=True
        )
        return JsonResponse(serializer.data, safe=False)
    else:
        # return JsonResponse({'invalid':"The user id provided by you doesnot have executive level"})
        return JsonResponse([], safe=False)


@api_view(['post'])
def get_company_sales(request):
    user_wise_sales = []
    total_sales = 0
    if request.data.get('year'):
        target_instance = Target.objects.filter(
            target_to__company_name__company_id=request.data.get('company_id'),
            year=request.data.get('year')
        )
        for i in target_instance:
            user_wise_sales.append({
                'name':i.target_to.user_name.first_name +' '+ i.target_to.user_name.last_name,
                'sales':i.sales})
            total_sales +=i.sales
        return JsonResponse({'total_sales':total_sales,
                            'user_wise_sales':user_wise_sales},
                            safe=False)
    else:
        target_instance = Target.objects.filter(
        target_to__company_name__company_id=request.data.get('company_id'),
        )
        for i in target_instance:
            user_wise_sales.append({
                'name':i.target_to.user_name.first_name +' '+ i.target_to.user_name.last_name,
                'sales':i.sales})
            total_sales +=i.sales
        return JsonResponse({'total_sales':total_sales,
                            'user_wise_sales':user_wise_sales},
                            safe=False)
    

class ExpensesViewset(viewsets.ModelViewSet):
    model = ExpenseData
    queryset = ExpenseData.objects.exclude(user_id__user_name__is_active=False)
    pagination_class = CustomPagination
    serializer_class = ExpensesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'user_id',
        'company_name'
        # 'mpo_tour_plan__tour_plan__tour_plan__select_the_month',
        # 'higher_order_tour_plan__month'
        ]
    
    @action(detail=False, methods=['POST'])
    def get_allowance_aggregation_mpo(self, request):
        user_id = request.data.get('user_id')
        month = request.data.get('month')
        year = request.data.get('year')
        monthly_expense_travel_allowance = ExpenseData.objects.filter(
            user_id=user_id,
            month=month,
            year=year
        ).aggregate(total=Sum('travel_allowance'))
        monthly_expense_daily_allowance = ExpenseData.objects.filter(
            user_id=user_id,
            month=month,
            year=year
        ).aggregate(total=Sum('daily_allowance'))
        monthly_travel_expense = monthly_expense_travel_allowance['total'] if monthly_expense_travel_allowance['total'] is not None else 0
        monthly_daily_expense = monthly_expense_daily_allowance['total'] if monthly_expense_daily_allowance['total'] is not None else 0
        total_allowance = (
            monthly_travel_expense + monthly_daily_expense)
        return Response(data={
            'travel_allowance': monthly_travel_expense,
            'daily_allowance': monthly_daily_expense,
            'total_allowance': total_allowance}, status=status.HTTP_200_OK)
