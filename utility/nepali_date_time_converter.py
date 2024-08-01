from django.db import models
import nepali_datetime as ndt


def convert_to_nepali_date(date_time):
    if date_time:
        # Assuming date_time is a datetime object
        nepali_date = ndt.datetime.from_datetime(date_time)
        return nepali_date.strftime("%Y-%m-%d %H:%M:%S")
    return None


class NepaliDateManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        for obj in queryset:
            if hasattr(obj, "created_at"):
                obj.nepali_created_at = convert_to_nepali_date(obj.created_at)
            if hasattr(obj, "updated_at"):
                obj.nepali_updated_at = convert_to_nepali_date(obj.updated_at)
            if hasattr(obj, "otp_created_at"):
                obj.otp_created_at = convert_to_nepali_date(obj.otp_created_at)
        return queryset
