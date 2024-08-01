from .models import ContactUs
from rest_framework import serializers


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
    
    def create(self, validated_data):
        return super().create(validated_data)