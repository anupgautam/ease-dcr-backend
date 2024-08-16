from datetime import datetime, timedelta

class BSDateConverter:
    bs_month_days = {
        2080: [31, 32, 31, 32, 31, 30, 30, 30, 29, 29, 30, 30],
        2081: [31, 32, 31, 32, 31, 30, 30, 30, 29, 30, 29, 31],
        # Add other years as needed
    }

    def __init__(self):
        self.ad_to_bs_start_date = datetime(2024, 8, 16)
        self.bs_start_year = 2080

    def convert_ad_to_bs(self, ad_date):
        ad_date = datetime.strptime(ad_date, '%Y-%m-%d')
        days_since_start = (ad_date - self.ad_to_bs_start_date).days

        # Calculate BS year
        days_per_year = 365
        bs_year = self.bs_start_year + (days_since_start // days_per_year)
        days_in_year = days_since_start % days_per_year

        # Calculate BS month and day
        days_accumulated = 0
        for month_index, days_in_month in enumerate(self.bs_month_days.get(bs_year, [])):
            if days_accumulated + days_in_month > days_in_year:
                bs_month = month_index + 1
                bs_day = days_in_year - days_accumulated + 1
                break
            days_accumulated += days_in_month

        return f"{bs_year}-{bs_month:02d}-{bs_day:02d}"

    def convert_bs_to_ad(self, bs_date):
        bs_date = datetime.strptime(bs_date, '%Y-%m-%d')
        bs_year = bs_date.year
        bs_month = bs_date.month
        bs_day = bs_date.day

        days_accumulated = sum(self.bs_month_days.get( [0] * 12)[:bs_month - 1]) + bs_day - 1
        days_since_start = (bs_year - self.bs_start_year) * 365 + days_accumulated

        # Calculate AD date
        ad_date = self.ad_to_bs_start_date + timedelta(days=days_since_start)
        return ad_date.strftime('%Y-%m-%d')
