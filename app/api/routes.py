from datetime import datetime
from flask import Blueprint, jsonify, request
from app.api.serializers import (api_response, serialize_advertiser,
                                serialize_application, serialize_order)
from app.services import AdvertiserService, ApplicationService, OrderService

api_blueprint = Blueprint('api_membership', __name__, url_prefix='/api_membership/')

advertiser_service = AdvertiserService()
application_service = ApplicationService(advertiser_service)
order_service = OrderService(application_service)


@api_blueprint.route('/advertisers', methods=['GET'])
def get_advertisers():
    """Retrieves the list of advertisers available to a publisher."""
    publisher_id = request.args.get('publisher_id')
    if not publisher_id:
        return api_response(
            message="Publisher login required",
            success=False,
            status_code=400
        )
    advertisers = advertiser_service.get_all_advertisers(publisher_id)
    serialized_advertisers = [serialize_advertiser(adv) for adv in advertisers]

    return api_response(
        data=serialized_advertisers,
        message=f"{len(serialized_advertisers)} advertisers found"
    )

@api_blueprint.route('/advertisers/<string:advertiser_id>', methods=['GET'])
def get_details_advertiser(advertiser_id):
    """Retrieves the details of an advertiser"""
    advertiser = advertiser_service.get_advertiser(advertiser_id)
    if not advertiser:
        return api_response(
            message="Advertiser not found",
            success=False,
            status_code=404
        )
    return api_response(
        data=serialize_advertiser(advertiser),
        message="Found advertiser"
    )

@api_blueprint.route('/advertisers/<string:advertiser_id>/tracking-url', methods=['GET'])
def get_tracking_url(advertiser_id):
    """Generates a tracking URL for an advertiser."""
    publisher_id = request.args.get('publisher_id')
    user_id = request.args.get('user_id')

    if not publisher_id or not user_id:
        return api_response(
            message='Login of advertiser & publisher required',
            success=False,
            status_code=400
        )

    if not application_service.check_publisher_access(publisher_id, advertiser_id):
        return api_response(
            message="Access to this advertiser is denied",
            success=False,
            status_code=403
        )

    custom_params = {key: value for key, value in request.args.items() if key not in ['publisher_id', 'user_id']}

    tracking_url = advertiser_service.get_advertiser_tracking_url(
        advertiser_id, publisher_id, user_id, custom_params
    )

    if not tracking_url:
        return api_response(
            message="Unable to generate tracking URL",
            success=False,
            status_code=400
        )

    return api_response(
        data={"tracking_url": tracking_url},
        message='Tracking URL generated successfully'
    )

@api_blueprint.route('/applications', methods=['GET'])
def get_applications():
    """Retrieves applications for a publisher"""
    publisher_id = request.args.get('publisher_id')
    if not publisher_id:
        return api_response(
            message="Publisher login required",
            success=False,
            status_code=400
        )

    applications = application_service.get_publisher_application(publisher_id)
    serialized_applications = [serialize_application(app) for app in applications]

    return api_response(
        data=serialized_applications,
        message=f"{len(serialized_applications)} applications found"
    )


@api_blueprint.route('/applications/<string:application_id>', methods=['GET'])
def get_application(application_id):
    """Retrieves the details of an application"""
    application = application_service.get_application(application_id)
    if not application:
        return api_response(
            message="Application not found",
            success=False,
            status_code=404
        )

    return api_response(
        data=serialize_application(application),
        message="Application found"
    )

@api_blueprint.route('/applications/<string:application_id>/approve', methods=['POST'])
def approve_application(application_id):
    """Automatically approve applications"""
    success, message = application_service.auto_approve_application(application_id)

    if not success:
        return api_response(
            message=message,
            success=False,
            status_code=400
        )

    return api_response(
        message=message
    )


@api_blueprint.route("/orders", methods=['GET'])
def get_orders():
    """Retrieves the orders of a publisher with optional filter"""
    publisher_id = request.args.get('publisher_id')
    if not publisher_id:
        return api_response(
            message="Publisher login required",
            success=False,
            status_code=400
        )

    advertiser_id = request.args.get('advertiser_id')

    from_date = None
    if request.args.get('from_date'):
        try:
            from_date = datetime.fromisoformat(request.args.get('from_date'))
        except (ValueError, TypeError):
            return api_response(
                message="Invalid start date format (ISO 8601 required)",
                success=False,
                status_code=400
            )

    to_date = None
    if request.args.get('to_date'):
        try:
            to_date = datetime.fromisoformat(request.args.get('to_date'))
        except (ValueError, TypeError):
            return api_response(
                message="Invalid end date format (ISO 8601 required)",
                success=False,
                status_code=400
            )

    orders = order_service.get_orders_for_publisher(
        publisher_id, advertiser_id, from_date, to_date
    )
    serialized_orders = [serialize_order(order) for order in orders]

    return api_response(
        data=serialized_orders,
        message=f"{len(serialized_orders)} orders found"
    )

@api_blueprint.route('/orders/track', methods=['POST'])
def track_order():
    """Simulates an order"""
    data = request.json
    if not data:
        return api_response(
            message="JSON data required",
            success=False,
            status_code=400
        )

    advertiser_id = data.get('advertiser_id')
    publisher_id = data.get('publisher_id')
    user_id = data.get('user_id')
    amount = data.get('amount')
    tracking_params = data.get('tracking_params')

    if not all([advertiser_id, publisher_id, user_id, amount]):
        return api_response(
            message="All mandatory fields must be completed",
            success=False,
            status_code=400
        )

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return api_response(
            message="The amount must be a number",
            success=False,
            status_code=400
        )

    order = order_service.track_order(
        advertiser_id, publisher_id, user_id, amount, tracking_params
    )

    if not order:
        return api_response(
            message="Unable to save the order",
            success=False,
            status_code=400
        )

    return api_response(
        data=serialize_order(order),
        message="Order successfully created",
        status_code=201
    )
