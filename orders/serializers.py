from rest_framework import serializers
from .models import Medication, Order

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Medication
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
