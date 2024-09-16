from datetime import datetime, timedelta

class BSDateConverter:
    bs_month_days = {
        2080: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        2081: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        2082: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2083: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        2084: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        2085: [31, 32, 31, 32, 30, 31, 30, 30, 29, 30, 30, 30],
        2086: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2087: [31, 31, 32, 31, 31, 31, 30, 30, 30, 30, 30, 30],
        2088: [30, 31, 32, 32, 30, 31, 30, 30, 29, 30, 30, 30],
        2089: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2090: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2091: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        2092: [30, 31, 32, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2093: [30, 32, 31, 32, 31, 30, 30, 30, 29, 30, 30, 30],
        2094: [31, 31, 32, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        2095: [31, 31, 32, 31, 31, 31, 30, 29, 30, 30, 30, 30],
        2096: [30, 31, 32, 32, 31, 30, 30, 29, 30, 29, 30, 30],
        2097: [31, 32, 31, 31, 31, 30, 30, 30, 29, 30, 30, 30],
        2098: [31, 31, 32, 31, 31, 31, 29, 30, 29, 30, 29, 31],
        2099: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 31],
    }

    def __init__(self):
        self.ad_to_bs_start_date = datetime(2023, 4, 14) 
        self.bs_start_year = 2080

    def convert_ad_to_bs_date(self, ad_date):
        ad_date = datetime.strptime(ad_date, '%Y-%m-%d')
        days_since_start = (ad_date - self.ad_to_bs_start_date).days

        bs_year = self.bs_start_year

        while days_since_start >= sum(self.bs_month_days[bs_year]):
            days_since_start -= sum(self.bs_month_days[bs_year])
            bs_year += 1

        for month_index, days_in_month in enumerate(self.bs_month_days[bs_year]):
            if days_since_start < days_in_month:
                bs_month = month_index + 1
                bs_day = days_since_start + 1
                break
            days_since_start -= days_in_month

        return f"{bs_year}-{bs_month:02d}-{bs_day:02d}"

    def convert_ad_to_bs(self, ad_date):
        ad_date = datetime.strptime(ad_date, '%Y-%m-%d')
        days_since_start = (ad_date - self.ad_to_bs_start_date).days

        bs_year = self.bs_start_year

        while days_since_start >= sum(self.bs_month_days[bs_year]):
            days_since_start -= sum(self.bs_month_days[bs_year])
            bs_year += 1

        for month_index, days_in_month in enumerate(self.bs_month_days[bs_year]):
            if days_since_start < days_in_month:
                bs_month = month_index + 1
                bs_day = days_since_start + 1
                break
            days_since_start -= days_in_month

        return f"{bs_year}-{bs_month:02d}-{bs_day:02d}"

    def convert_bs_to_ad(self, bs_date):
        if isinstance(bs_date, datetime):
            date = bs_date.strftime('%Y-%m-%d')
        elif isinstance(bs_date, str):
            date = bs_date
        else:
            raise ValueError("bs_date must be either a string or a date object")
        date = bs_date.strftime('%Y-%m-%d')
        bs_year, bs_month, bs_day = map(int, date.split('-'))

        days_accumulated = sum(self.bs_month_days.get(bs_year, [])[0:bs_month - 1]) + bs_day - 1

        days_since_start = 0
        for year in range(self.bs_start_year, bs_year):
            days_since_start += sum(self.bs_month_days.get(year, [])) 

        days_since_start += days_accumulated

        ad_date = self.ad_to_bs_start_date + timedelta(days=days_since_start)
        return ad_date.strftime('%Y-%m-%d')
