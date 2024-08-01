from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from sales.models import SecondarySales, PrimarySales
from sales.serializers import SecondarySalesSerializers, PrimarySalesSerializers

# Create your views here.

class SecondarySalesViewsets(viewsets.ModelViewSet):
    model = SecondarySales
    queryset = SecondarySales.objects.all()
    serializer_class = SecondarySalesSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'stockist', 'year', 'month','company_name']


class PrimarySalesViewsets(viewsets.ModelViewSet):
    model = PrimarySales
    queryset = PrimarySales.objects.all()
    serializer_class = PrimarySalesSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'stockist', 'year', 'month','company_name']
