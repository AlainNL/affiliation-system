from datetime import datetime
from flask import Blueprint, jsonify, request
from app.api.serializers import (api_response, serialize_advertiser,
                                serialize_application, serialize_order)
from app.services import AdvertiserService, ApplicationService, OrderService

api_blueprint = Blueprint('api_membership', __name__, url_prefix='/api_membership/')

advertiser_service = AdvertiserService()
application_service = ApplicationService(advertiser_service)
order_service = OrderService(application_service)

# Récupérer les informations d’un annonceur
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

# Récupérer les détails d’un annonceur
@api_blueprint.route('/advertisers/<string:advertiser_id>', methods=['GET'])
def get_details_advertiser(advertiser_id):
    """Retrieves the details of an advertiser."""
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

# Candidater à un annonceur
@api_blueprint.route('/applications', methods=['POST'])
def apply_to_advertiser():
    """Allows a publisher to apply to an advertiser."""
    publisher_id = request.json.get('publisher_id')
    advertiser_id = request.json.get('advertiser_id')

    if not publisher_id or not advertiser_id:
        return api_response(
            message="Publisher and advertiser IDs are required",
            success=False,
            status_code=400
        )

    # Appel de la méthode apply_to_advertiser
    success, message, application = application_service.apply_to_advertiser(publisher_id, advertiser_id)

    # Retour de la réponse en fonction du résultat
    if not success:
        return api_response(
            message=message,
            success=success,
            status_code=400
        )

    # Si l'application est réussie, vous pouvez retourner les informations de l'application
    return api_response(
        message=message,
        success=success,
        data={'application_id': application.id, 'advertiser_id': application.advertiser_id},
        status_code=201
    )

# Récupérer les commandes attribuées à un éditeur
@api_blueprint.route('/orders', methods=['GET'])
def get_orders():
    """Retrieves the orders of a publisher with optional filter."""
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

# Simuler une commande (suivi)
@api_blueprint.route('/orders/track', methods=['POST'])
def track_order():
    """Simulates an order."""
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
