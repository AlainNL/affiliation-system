from datetime import datetime
from typing import Dict, List, Union
from flask import jsonify
from app.models.advertiser import Advertiser
from app.models.application import Application
from app.models.order import Order

def serialize_datetime(dt: datetime) -> str:
    """Convert datetime in ISO format"""
    return dt.isoformat() if dt else None

def serialize_advertiser(advertiser: Advertiser) -> Dict:
    """
    Convert Advertiser for JSON serializer

    Args:
        Object Advertiser

    Returns:
        Dictionary representing the advertiser
    """
    return {
        "id": advertiser.id,
        "name": advertiser.name,
        "description": advertiser.description,
        "website": advertiser.website,
        "commission_rate": advertiser.commission_rate,
        "category": advertiser.category,
        "is_active": advertiser.is_active
    }

def serialize_application(application: Application) -> Dict:
    """
    Convert Application for JSON serializer

    Args:
        Object Application

    Returns:
        Dictionary representing an application
    """
    return {
        "id": application.id,
        "advertiser_id": application.advertiser_id,
        "publisher_id": application.publisher_id,
        "status": application.status.values,
        "application_date": serialize_datetime(application.application_date),
        "responte_date": serialize_datetime(application.response_datedate),
        "notes": application.notes
    }

def serialize_order(order: Order) -> Dict:
    """
    Convert Order for JSON serializer

    Args:
        Object Order
    Returns:
        Dictionary representing an order
    """
    return {
        "id": order.id,
        "advertiser_id": order.advertiser_id,
        "publisher_id": order.publisher_id,
        "user_id": order.user_id,
        "amount": order.amount,
        "commission": order.commission,
        "status": order.status.value,
        "order_date": serialize_datetime(order.order_date),
        "validation_date": serialize_datetime(order.validation_date),
        "tracking_params": order.tracking_params
    }

def api_response(data: Union[Dict, List, None] = None, message: str = "",
                success: bool = True, status_code: int = 200) -> tuple:
    """
    Create a standart API response

    Args:
        data: data including in response
        message
        success
        status_code: status code HTTP

    Returns:
        Tuple with response JSON + status code
    """
    respone ={
        "success": success,
        "message": message,
        "data": data
    }
    return jsonify(respone),status_code
