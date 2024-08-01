import datetime
from django.utils import timezone

def calender():
    todays_date = timezone.now().date()
    
    all_date = {
        "date":[
            {"date":""}
        ]
    }
    first = all_date["date"]
    
    second=(first[0])
    second = second["date"]
    
    
    for i in range(30):
        next_date = todays_date + datetime.timedelta(days=i)
        all_date["date"][0] = next_date
    
    
    
    return all_date
    