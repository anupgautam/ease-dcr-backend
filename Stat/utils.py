from datetime import datetime

from dailycallrecord.utils import nepali_month_to_digit

def get_nepali_dates_for_month(year, month):
    month = nepali_month_to_digit(month)
    # Determine the number of days in the given month
    if month != 12:
        num_days = (datetime(year, month % 12 + 1, 1) - datetime(year, month, 1)).days
    else:
        num_days = (datetime(year + 1, 1, 1) - datetime(year, month, 1)).days
    
    # Generate datetime objects for each day of the month
    dates = [datetime(year, month, day) for day in range(1, num_days + 1)]
    date_dict = {}
    for date in dates:
        date_dict[date] = ''
    return date_dict