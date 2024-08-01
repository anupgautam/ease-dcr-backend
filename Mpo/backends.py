from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

class CaseInsensitiveDjangoFilterBackend(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_fields = getattr(view, 'filter_fields', None)
        if not filter_fields:
            return queryset
        filters = {}
        for param, value in request.query_params.items():
            if param in filter_fields:
                if value == None or value == "":
                    pass

                else:
                    if param in getattr(view, 'case_insensitive_fields', []):
                        filters[param + '__iexact'] = value
                    else:
                        filters[param] = value
        return queryset.filter(**filters)
    