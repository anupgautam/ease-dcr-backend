from rest_framework import serializers

from sales.models import SecondarySales, PrimarySales


class SecondarySalesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = SecondarySales
        fields = "__all__"


class PrimarySalesSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = PrimarySales
        fields = "__all__"