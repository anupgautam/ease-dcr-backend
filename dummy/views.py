from rest_framework import viewsets
from .serializers import *
from .models import *
from .utils import country_and_city_data_transmission
from rest_framework.response import Response


class CountryViewset(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewset(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    def create(self, request, *args, **kwargs):
        data = country_and_city_data_transmission(request)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        instance = City.objects.get(id=id)
        data = country_and_city_data_transmission(request)
        serializer = CitySerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)