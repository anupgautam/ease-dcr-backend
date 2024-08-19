from django.db import models
from datetime import date
from django.core import exceptions
from django import forms


class BSDateField(models.Field):
    empty_strings_allowed = False
    default_error_messages = {
        'invalid': (
            "“%(value)s” value has an invalid BS date format. It must be a valid BS date (e.g., 2079-01-31, 2079-04-32)."
        ),
        'invalid_date': (
            "“%(value)s” value has the correct format (YYYY-MM-DD) but it is an invalid BS date (months can have 30-32 days)."
        ),
    }
    description = ("BS Date (Bikram Sambat)")

    def __init__(self, verbose_name=None, name=None, auto_now=False, auto_now_add=False, **kwargs):
        super().__init__(verbose_name=verbose_name, name=name, auto_now=auto_now, auto_now_add=auto_now_add, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            try:
                year, month, day = map(int, value.split('-'))
                # Validate BS month range (30-32)
                if not (1 <= month <= 12 and 1 <= day <= self._get_max_day_of_month(year, month)):
                    raise ValueError('Invalid BS date format (month out of range).')
                return date(year, month, day)
            except (ValueError, TypeError):
                raise exceptions.ValidationError(self.error_messages['invalid'], params={'value': value}, code='invalid')
        else:
            raise exceptions.ValidationError(self.error_messages['invalid'], params={'value': value}, code='invalid')

    def _get_max_day_of_month(self, year, month):
        # Logic to determine the maximum number of days in a BS month (replace with your implementation)
        # Example (assuming a fixed cycle of 31-day and 32-day months):
        bs_month_lengths = [31, 32] * 6 + [31]  # Repeat the cycle for practicality
        return bs_month_lengths[month - 1]

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        # Adapt value for database storage (if necessary)
        if not prepared:
            value = self.get_prep_value(value)
        return connection.ops.adapt_datefield_value(value)

    def formfield(self, **kwargs):
        kwargs['form_class'] = forms.DateField  # Use standard DateField form
        return super().formfield(**kwargs)