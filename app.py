import logging
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

import shopify
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pyactiveresource.connection import ResourceNotFound  # Import here

load_dotenv()

SHOP_NAME = os.getenv("SHOPIFY_SHOP_NAME")
ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
API_VERSION = '2023-10'

if not all([ACCESS_TOKEN, SHOP_NAME]):
    raise EnvironmentError("Missing Shopify API credentials in .env file.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Mask sensitive info
logger.info(f"Access Token Prefix: {ACCESS_TOKEN[:4]}...")
logger.info(f"Shop Name: {SHOP_NAME}")

app = FastAPI()

def activate_shopify_session():
    session = shopify.Session(f"{SHOP_NAME}.myshopify.com", API_VERSION, ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)
    logger.debug(f"Activated session for shop: {session.site}")

@app.get("/orders")
def get_orders():
    try:
        activate_shopify_session()
        orders = shopify.Order.find(limit=250)
        return [order.to_dict() for order in orders]
    except Exception as e:
        logger.error("Error fetching orders", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shopify.ShopifyResource.clear_session()

@app.get("/orders/{order_id}")
def get_order(order_id: int):
    try:
        activate_shopify_session()
        order = shopify.Order.find(order_id)
        return order.to_dict()
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Order not found")
    except Exception as e:
        logger.error("Error fetching order", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shopify.ShopifyResource.clear_session()

@app.get("/customers")
def get_customers():
    try:
        activate_shopify_session()
        customers = shopify.Customer.find(limit=250)
        return [customer.to_dict() for customer in customers]
    except Exception as e:
        logger.error("Error fetching customers", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shopify.ShopifyResource.clear_session()

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    try:
        activate_shopify_session()
        customer = shopify.Customer.find(customer_id)
        return customer.to_dict()
    except ResourceNotFound:
        raise HTTPException(status_code=404, detail="Customer not found")
    except Exception as e:
        logger.error("Error fetching customer", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        shopify.ShopifyResource.clear_session()
