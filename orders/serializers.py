from rest_framework import serializers
from .models import Medication, Order, Statement
from . import models

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Medication
        fields = '__all__'
        
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        

class StatementSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Statement
        fields = '__all__'
        

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transaction
        fields = "__all__"