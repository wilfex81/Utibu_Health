import base64
import logging
import time
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import math
import os

from orders.models import Transaction

logging = logging.getLogger("default")

class MpesaGateWay:
    shortcode = None
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiration = None
    checkout_url = None
    timestamp = None


    def __init__(self):
        now = datetime.now()
        self.shortcode = os.environ.get("shortcode")
        self.consumer_key = os.environ.get("consumer_key")
        self.consumer_secret = os.environ.get("consumer_secret")
        self.access_token_url = os.environ.get("access_token_url")

        self.password = self.generate_password()
        self.c2b_callback = os.environ.get("c2b_callback")
        self.checkout_url = os.environ.get("checkout_url")

        try:
            self.access_token = self.getAccessToken()
            if self.access_token is None:
                raise Exception("Request for access token failed.")
        except Exception as e:
            logging.error("Error {}".format(e))
        else:
            self.access_token_expiration = time.time() + 3400

    def getAccessToken(self):
        try:
            res = requests.get(
                self.access_token_url,
                auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
            )
        except Exception as err:
            logging.error("Error {}".format(err))
            raise err
        else:
            token = res.json()["access_token"]
            self.headers = {"Authorization": "Bearer %s" % token}
            return token

    class Decorators:
        @staticmethod
        def refreshToken(decorated):
            def wrapper(gateway, *args, **kwargs):
                if (
                    gateway.access_token_expiration
                    and time.time() > gateway.access_token_expiration
                ):
                    token = gateway.getAccessToken()
                    gateway.access_token = token
                return decorated(gateway, *args, **kwargs)

            return wrapper


    def generate_password(self):
        """Generates mpesa api password using the provided shortcode and passkey"""
        self.timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str =  self.timestamp
        password_bytes = password_str.encode("ascii")
        return base64.b64encode(password_bytes).decode("utf-8")

    @Decorators.refreshToken
    def stk_push_request(self, payload):
        request = payload["request"]
        data = payload["data"]
        amount = data["amount"]
        phone_number = data["phone_number"]
        req_data = {
            "BusinessShortCode": self.shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.c2b_callback,
            "AccountReference": "Test",
            "TransactionDesc": "Test",
        }

        res = requests.post(
            self.checkout_url, json=req_data, timeout=30
        )
        res_data = res.json()
        logging.info("Mpesa request data {}".format(req_data))
        logging.info("Mpesa response info {}".format(res_data))

        if res.ok:
            data["ip"] = request.META.get("REMOTE_ADDR")
            data["checkout_request_id"] = res_data["CheckoutRequestID"]

            Transaction.objects.create(**data)
        return res_data