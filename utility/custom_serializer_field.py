from rest_framework import serializers

class ModelCustomField(serializers.Field):

    def __init__(self, model_name):
        self.model_name = model_name

    def to_internal_value(self, data):
        
        # validate and convert the data during deserialization
        try:
            return self.model_name.objects.get(pk=data)
        except:
            raise serializers.ValidationError("invalid primary key")

    def to_representation(self, value):
        # validate and convert the data during serialization
        if not isinstance(value, str):
            raise serializers.ValidationError("Invalid data type")
        return value
