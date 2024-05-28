#!/usr/bin/python3
"""Returns the status of an API."""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Return the status of the API.

    Returns:
        A JSON object containing the status of the API.
    """
    return {'status': 'OK'}


@app_views.route('/stats', strict_slashes=False)
def api_stats():
    """Return the number of each object by type.

    Returns:
        A JSON object containing the number of each object by type.
    """
    return jsonify({
        'amenities': storage.count("Amenity"),
        'cities': storage.count("City"),
        'places': storage.count("Place"),
        'reviews': storage.count("Review"),
        'states': storage.count("State"),
        'users': storage.count("User")
    })
