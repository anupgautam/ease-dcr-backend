from datetime import datetime, timedelta, date
from abc import ABC, abstractmethod

from django.utils import timezone    

class DateUtils(ABC):
    
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_yesterday_date(self):
        pass

    @abstractmethod
    def get_first_date_of_the_week(self):
        pass

    @abstractmethod
    def get_last_date_of_the_week(self):
        pass


class DateUtilsWithDate(DateUtils):
    
    def __init__(self) -> None:
        super().__init__()

    def get_yesterday_date(self):
        current_datetime = timezone.now()
        yesterday_date = current_datetime - timedelta(days=1)
        yesterday_date_only = yesterday_date.date() 
        return yesterday_date_only

    def get_first_date_of_the_week(self):
        current_date = datetime.now().date()
        start_date = current_date - timedelta(days=7)
        first_date = (start_date + timedelta(days=0)).strftime(
            '%Y-%m-%d')
        return first_date

    def get_last_date_of_the_week(self):
        current_date = datetime.now().date()
        start_date = current_date - timedelta(days=7)
        last_date = start_date + timedelta(days=6)
        return last_date