#!/usr/bin/python3
"""
Creates a new view for state object
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, request, make_response, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all state objects"""
    states = storage.all(State)
    return jsonify({'states': list(states.values())})


@app_views.route('/states/<int:state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state object"""
    state = storage.get(State, state_id)
    if state is not None:
        return jsonify(state.to_dict())
    else:
        return jsonify({}), 404


@app_views.route('/states/<int:state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return jsonify({}), 404


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<int:state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
