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
        self.ad_to_bs_start_date = datetime(2024, 8, 16)
        self.bs_start_year = 2080

    def convert_ad_to_bs(self, ad_date):
        ad_date = datetime.strptime(ad_date, '%Y-%m-%d')
        days_since_start = (ad_date - self.ad_to_bs_start_date).days

        bs_year = self.bs_start_year

        # Calculate BS year
        while True:
            year_days = sum(self.bs_month_days[bs_year])
            if days_since_start < year_days:
                break
            days_since_start -= year_days
            bs_year += 1

        # Calculate BS month and day
        bs_month = 0
        for month_days in self.bs_month_days[bs_year]:
            if days_since_start < month_days:
                break
            days_since_start -= month_days
            bs_month += 1

        bs_month += 1
        bs_day = days_since_start + 1

        return f"{bs_year}-{bs_month:02d}-{bs_day:02d}"

    def convert_bs_to_ad(self, bs_date):
        bs_date = datetime.strptime(bs_date, '%Y-%m-%d')
        bs_year = bs_date.year
        bs_month = bs_date.month
        bs_day = bs_date.day

        days_since_start = 0

        # Accumulate days for all years up to the given BS year
        for year in range(self.bs_start_year, bs_year):
            days_since_start += sum(self.bs_month_days[year])

        # Accumulate days for all months in the current BS year
        days_since_start += sum(self.bs_month_days[bs_year][:bs_month - 1])

        # Add the days in the current BS month
        days_since_start += bs_day - 1

        # Calculate AD date
        ad_date = self.ad_to_bs_start_date + timedelta(days=days_since_start)
        return ad_date.strftime('%Y-%m-%d')
