#!/usr/bin/python3
""" """

from api.v1.views import app_views
from models import storage
from models.city import City
from flask import jsonify, request, abort


@app_views.route('/states/<int:state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieves the list of all city objects"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<int:city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a city object"""
    data = request.get_json()
    if not data:
        abort(404)
    return jsonify(storage.city.get(city_id).to_dict())


@app_views.route('/cities/<int:city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object"""
    data = request.get_json()
    if not data:
        abort(404)
    storage.delete(storage.city.get(city_id))
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<int:state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new City object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<int:city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at',
                       'updated_at']
        setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
