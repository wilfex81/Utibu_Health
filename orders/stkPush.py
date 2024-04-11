import requests
from datetime import datetime
import json
import base64
from django.http import JsonResponse
from .genrateAcesstoken import get_access_token
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


class STKPushAPiView(APIView):
    @swagger_auto_schema(
        operation_summary='Initiate STK Push to Intiate Payments',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="STK Push initiated successfully",
                examples={
                    "application/json": {
                        "CheckoutRequestID": "123456789",
                        "ResponseCode": "0"
                    }
                }
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "STK push failed."
                    }
                }
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                examples={
                    "application/json": {
                        "error": "Internal server error occurred."
                    }
                }
            )
        }
    )
    def initiate_stk_push(request):
        '''
        Handle STK push to initiate payments
        
        '''
        access_token_response = get_access_token(request)
        if isinstance(access_token_response, JsonResponse):
            access_token = access_token_response.content.decode('utf-8')
            access_token_json = json.loads(access_token)
            access_token = access_token_json.get('access_token')
            if access_token:
                amount = 1
                phone = "254798630738"
                passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
                business_short_code = '174379'
                process_request_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                callback_url = 'https://crystalcleanesentials.com/callback'
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                password = base64.b64encode((business_short_code + passkey + timestamp).encode()).decode()
                party_a = phone
                party_b = '254798630738'
                account_reference = 'CRYSTALCLEAN ESSENTIALS'
                transaction_desc = 'stkpush test'
                stk_push_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + access_token
                }
                
                stk_push_payload = {
                    'BusinessShortCode': business_short_code,
                    'Password': password,
                    'Timestamp': timestamp,
                    'TransactionType': 'CustomerPayBillOnline',
                    'Amount': amount,
                    'PartyA': party_a,
                    'PartyB': business_short_code,
                    'PhoneNumber': party_a,
                    'CallBackURL': callback_url,
                    'AccountReference': account_reference,
                    'TransactionDesc': transaction_desc
                }

                try:
                    response = requests.post(process_request_url, headers=stk_push_headers, json=stk_push_payload)
                    response.raise_for_status()   
                    response_data = response.json()
                    checkout_request_id = response_data['CheckoutRequestID']
                    response_code = response_data['ResponseCode']
                    
                    if response_code == "0":
                        return JsonResponse({'CheckoutRequestID': checkout_request_id, 'ResponseCode': response_code})
                    else:
                        return JsonResponse({'error': 'STK push failed.'})
                except requests.exceptions.RequestException as e:
                    return JsonResponse({'error': str(e)})
            else:
                return JsonResponse({'error': 'Access token not found.'})
        else:
            return JsonResponse({'error': 'Failed to retrieve access token.'})