
from django.urls import path
from .views import (OrderListCreateAPIView, OrderDetailAPIView,MedicationListCreateAPIView, 
                        MedicationDetailAPIView,StatementDetailAPIView,UserRegistrationAPIView, 
                        UserLoginAPIView,UserLogoutAPIView,STKPushAPiView)
from . import views
urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user_register'),
    path('login/', UserLoginAPIView.as_view(), name='user_login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('medications/', MedicationListCreateAPIView.as_view(), name='medication-list-create'),
    path('medications/<int:pk>/', MedicationDetailAPIView.as_view(), name='medication-detail'),
    path('statement/<int:pk>/', StatementDetailAPIView.as_view(), name='statement-detail'),
    path('accesstoken/', views.get_access_token, name='get_access_token'),
    path('stkpush/', views.initiate_stk_push, name='initiate_stk_push'),
    path('stkpush/', STKPushAPiView.as_view(),name = 'stk_push'),
]
