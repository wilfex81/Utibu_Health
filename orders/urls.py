
from django.urls import path
from .views import (OrderListCreateAPIView, OrderDetailAPIView,MedicationListCreateAPIView, 
                        MedicationDetailAPIView,StatementDetailAPIView)

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('medications/', MedicationListCreateAPIView.as_view(), name='medication-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
    path('statement/<int:pk>/', StatementDetailAPIView.as_view(), name='statement-detail'),
]
