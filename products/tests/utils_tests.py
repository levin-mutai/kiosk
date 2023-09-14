
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from utils.notification import SMS

# test sending SMS

def test_sedning_SMS():
    messsage = "Hello World!"
    try:
        resp = SMS.send_sms(messsage)
        assert resp.status_code == 200 
    except Exception as e:
        print(e)
        assert False