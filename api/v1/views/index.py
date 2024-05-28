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
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """Return the number of each object by type.

    Returns:
        A JSON object containing the number of each object by type.
    """
    from models.user import User
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    return jsonify({
        'amenities': storage.count(Amenity),
        'cities': storage.count(City),
        'places': storage.count(Place),
        'reviews': storage.count(Review),
        'states': storage.count(State),
        'users': storage.count(User)
    })
