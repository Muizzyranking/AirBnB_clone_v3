#!/usr/bin/python3
"""views that handles all restful api actions for places"""
from app.v1.views import app_views
from models import storage, Place
from flask import jsonify, request, abort, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """get all places by city id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = city.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get a place by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.json:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", request.json['user_id'])
    if user is None:
        abort(404)
    if 'name' not in request.json:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place = Place(**request.json())
    place.city_id = city_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    atributes = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    if place is None:
        abort(404)
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.json.items():
        if attr not in atributes:
            setattr(place, attr, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
