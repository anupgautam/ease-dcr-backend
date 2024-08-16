from rest_framework import serializers

class DateConversionSerializer(serializers.Serializer):
    ad_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    bs_date = serializers.DateField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'], required=False)