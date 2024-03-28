# views.py
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Medication, Order
from .serializers import MedicationSerializer, OrderSerializer

class OrderListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="List orders",
        responses={status.HTTP_200_OK: openapi.Response('List of orders', OrderSerializer(many=True))}
    )
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create order",
        request_body=OrderSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response('Created order', OrderSerializer)}
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailAPIView(APIView):
    def get_order(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
        
    @swagger_auto_schema(
        operation_summary="Retrieve order details",
        responses={status.HTTP_200_OK: openapi.Response('Order details', OrderSerializer)}
    )
    def get(self, request, pk):
        order = self.get_order(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update order",
        request_body=OrderSerializer,
        responses={status.HTTP_200_OK: openapi.Response('Updated order', OrderSerializer)}
    )
    def put(self, request, pk):
        order = self.get_order(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete order",
        responses={status.HTTP_204_NO_CONTENT: "No Content"}
    )
    def delete(self, request, pk):
        order = self.get_order(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MedicationListCreateAPIView(APIView):
    '''
    Pharmacy/Doctor can create medication(s)
    for a patient with this endpoint
    '''
    @swagger_auto_schema(
        operation_summary='Medication List',
        responses={status.HTTP_200_OK: openapi.Response('List of Medications',MedicationSerializer(many=True))}    
    )
    def get(self, request):
        medication = Medication.objects.all()
        serializer = MedicationSerializer(medication, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Create Medication",
        request_body=MedicationSerializer,
        responses={
            status.HTTP_201_CREATED:openapi.Response('Created Medication', MedicationSerializer)
        }
    )
    def post(self, request):
        serializer = MedicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
class MedicationDetailAPIView(APIView):
    '''
    with this endpoint the patient can select a given 
    medication as per the doctors prescription
    The doctor can also update or delete a given medication for a given customer
    '''
    
    def get_medication(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404
    
    @swagger_auto_schema(
        operation_summary='Retrieve Medication details',
        responses={
            status.HTTP_200_OK:openapi.Response('Medication details', MedicationSerializer)
        }
    )
    def get(self, request, pk):
        medication = self.get_medication(pk)
        serializer = MedicationSerializer(medication)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Update Medication",
        request_body=MedicationSerializer,
        responses={
            status.HTTP_200_OK:openapi.Response('Updates Medication', MedicationSerializer)
        }
    )
    def put(self, request, pk):
        medication = self.get_medication(pk)
        serializer = MedicationSerializer(medication, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_summary="Delete a given Medication",
        responses={
            status.HTTP_204_NO_CONTENT: "No Content"
        }
    )
    def delete(self, request, pk):
        medication = self.get_medication(pk)
        medication.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    