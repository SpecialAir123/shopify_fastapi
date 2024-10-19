import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from pyactiveresource.connection import ResourceNotFound
import pytest

from app import app

client = TestClient(app)

def test_get_orders():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch('shopify.Order.find')
def test_get_order_not_found(mock_find):
    mock_response = Mock()
    mock_response.code = 404
    mock_response.msg = 'Not Found'
    mock_response.headers = {'Content-Type': 'application/json'}
    mock_response.url = 'https://example.com/orders/99999999.json'
    mock_response.read.return_value = b'{"errors":"Not Found"}'
    mock_find.side_effect = ResourceNotFound(response=mock_response)
    response = client.get("/orders/99999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Order not found"}

@patch('shopify.Order.find')
def test_get_order_success(mock_find):
    mock_order = Mock()
    mock_order.to_dict.return_value = {
        "id": 123456789,
        "email": "customer@example.com",
        "total_price": "100.00",
    }
    mock_find.return_value = mock_order

    response = client.get("/orders/123456789")
    assert response.status_code == 200
    assert response.json() == {
        "id": 123456789,
        "email": "customer@example.com",
        "total_price": "100.00",
    }

@patch('shopify.Order.find')
def test_get_orders_exception(mock_find):
    mock_find.side_effect = Exception("Test exception")

    response = client.get("/orders")
    assert response.status_code == 500
    assert "Test exception" in response.json()["detail"]

def test_get_order_invalid_id():
    response = client.get("/orders/invalid-id")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

def test_get_customers():
    response = client.get("/customers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch('shopify.Customer.find')
def test_get_customer_not_found(mock_find):
    mock_response = Mock()
    mock_response.code = 404
    mock_response.msg = 'Not Found'
    mock_response.headers = {'Content-Type': 'application/json'}
    mock_response.url = 'https://example.com/customers/99999999.json'
    mock_response.read.return_value = b'{"errors":"Not Found"}'
    mock_find.side_effect = ResourceNotFound(response=mock_response)
    response = client.get("/customers/99999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}

@patch('shopify.Customer.find')
def test_get_customer_success(mock_find):
    mock_customer = Mock()
    mock_customer.to_dict.return_value = {
        "id": 987654321,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }
    mock_find.return_value = mock_customer

    response = client.get("/customers/987654321")
    assert response.status_code == 200
    assert response.json() == {
        "id": 987654321,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
    }

@patch('shopify.Customer.find')
def test_get_customers_exception(mock_find):
    mock_find.side_effect = Exception("Test exception")

    response = client.get("/customers")
    assert response.status_code == 500
    assert "Test exception" in response.json()["detail"]

def test_get_customer_invalid_id():
    response = client.get("/customers/invalid-id")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

@patch('shopify.Order.find')
def test_get_orders_mock(mock_find):
    mock_find.return_value = []
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.json() == []

@patch('shopify.Customer.find')
def test_get_customers_mock(mock_find):
    mock_find.return_value = []
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == []

def test_missing_environment_variables():
    with patch.dict(os.environ, {"SHOPIFY_ACCESS_TOKEN": "", "SHOPIFY_SHOP_NAME": ""}):
        with pytest.raises(EnvironmentError) as excinfo:
            # Re-import the app module to trigger the environment check
            import importlib
            import app
            importlib.reload(app)
        assert "Missing Shopify API credentials" in str(excinfo.value)
