from rest_framework import serializers
from .models import TransformedData

class TransformedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformedData
        fields = '__all__'
