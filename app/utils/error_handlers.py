from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        """Handles 400 Bad Request errors."""
        return jsonify({
            'success': False,
            'message': 'Bad request',
            'error': str(error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        """Handles 404 Not Found errors."""
        return jsonify({
            'success': False,
            'message': 'Resource not found',
            'error': str(error)
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handles 405 Method Not Allowed errors."""
        return jsonify({
            'success': False,
            'message': 'Method not allowed',
            'error': str(error)
        }), 405

    @app.errorhandler(500)
    def server_error(error):
        """Handles 500 Internal Server Error errors."""
        return jsonify({
            'success': False,
            'message': 'Internal server error',
            'error': str(error)
        }), 500
