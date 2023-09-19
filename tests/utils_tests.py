import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from products.utils.notification import SMS

# # test sending SMS


def test_sedning_SMS():
    messsage = "Hello World!"
    try:
        resp = SMS.send_sms(messsage)
        assert resp.status_code == 200
    except Exception as e:
        print(e)
        assert False


def test_sum_positive_numbers():
    result = sum([2, 3])
    assert result == 5


def test_sum_negative_numbers():
    result = sum([-2, -3])
    assert result == -5


def test_sum_mixed_numbers():
    result = sum([2, -3])
    assert result == -1
