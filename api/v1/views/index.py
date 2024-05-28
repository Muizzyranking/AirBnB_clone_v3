#!/usr/bin/python3
"""Returns the status of an API."""

from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """Return the status of the API.

    Returns:
        A JSON object containing the status of the API.
    """
    return {'status': 'OK'}

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
    return {
        'amenities': len(storage.all(Amenity).values()),
        'cities': len(storage.all(City).values()),
        'places': len(storage.all(Place).values()),
        'reviews': len(storage.all(Review).values()),
        'states': len(storage.all(State).values()),
        'users': len(storage.all(User).values())
    }
