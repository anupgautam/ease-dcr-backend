# bsdate/fields.py

from django.db import models
from django.core.exceptions import ValidationError
from bsdate.convertor import BSDateConverter

class BSDateField(models.CharField):
    # description = "A date field for Bikram Sambat calendar"
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # Format: YYYY-MM-DD
        super().__init__(*args, **kwargs)
        self.converter = BSDateConverter()

    def to_python(self, value):
        if not value:
            return None
        try:
            # Validate BS date format
            year, month, day = map(int, value.split('-'))
            if month < 1 or month > 12:
                raise ValidationError("Invalid month in BS date.")
            if day < 1 or day > self.converter.bs_month_days.get(year, [])[month - 1]:
                raise ValidationError("Invalid day in BS date.")
            return value
        except (ValueError, TypeError, IndexError):
            raise ValidationError("Invalid BS date format.")

    def get_prep_value(self, value):
        return super().get_prep_value(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value
