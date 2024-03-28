# views.py
from django.contrib.auth import logout
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Medication, Order, Statement
from .serializers import MedicationSerializer, OrderSerializer, StatementSerializer


class UserRegistrationAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="User Registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "email", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: "Created",
            400: "Bad Request",
        },
    )
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({"error": "Please provide username, email, and password"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username is already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username, email=email, password=password)
        if user:
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Unable to register user"}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="User Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: "OK",
            401: "Unauthorized",
        },
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Please provide username and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class OrderListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_summary="List orders",
        responses={status.HTTP_200_OK: openapi.Response(
            'List of orders', OrderSerializer(many=True))}
    )
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create order",
        request_body=OrderSerializer,
        responses={status.HTTP_201_CREATED: openapi.Response(
            'Created order', OrderSerializer)}
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
        responses={status.HTTP_200_OK: openapi.Response(
            'Order details', OrderSerializer)}
    )
    def get(self, request, pk):
        order = self.get_order(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Update order",
        request_body=OrderSerializer,
        responses={status.HTTP_200_OK: openapi.Response(
            'Updated order', OrderSerializer)}
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
        responses={status.HTTP_200_OK: openapi.Response(
            'List of Medications', MedicationSerializer(many=True))}
    )
    def get(self, request):
        medication = Medication.objects.all()
        serializer = MedicationSerializer(medication, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create Medication",
        request_body=MedicationSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                'Created Medication', MedicationSerializer)
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
            return Medication.objects.get(pk=pk)
        except Medication.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary='Retrieve Medication details',
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Medication details', MedicationSerializer)
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
            status.HTTP_200_OK: openapi.Response(
                'Updates Medication', MedicationSerializer)
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


class StatementDetailAPIView(APIView):
    '''
    Patient gets a statement of pending bills
    '''

    def get_statement(self, pk):
        try:
            return Statement.objects.get(pk=pk)
        except Statement.DoesNotExist:
            raise Http404

    @swagger_auto_schema(
        operation_summary='Retrieve Statement details',
        responses={
            status.HTTP_200_OK: openapi.Response(
                'Statement Details', StatementSerializer)
        }
    )
    def get(self, request, pk):
        statement = self.get_statement(pk)
        serializer = StatementSerializer(statement)
        return Response(serializer.data)
