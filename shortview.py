#!/usr/bin/python3
"States module"
from flask import jsonify, request, Response, abort
from api.v1.views import app_views
from models import storage
import json
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_all_states():
    "returns all states"
    states = storage.all("State").values()

    return jsonify([state.to_dict() for state in states])


@app_views.route(
    '/states/<string:state_id>',
    strict_slashes=False,
    methods=['GET'])
def get_a_states(state_id):
    "returns a state by id"
    state = storage.get("State", state_id)

    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route(
    '/states/<string:state_id>',
    strict_slashes=False,
    methods=['DELETE'])
def delete_a_states(state_id):
    'deletes a state'
    state = storage.get("State", state_id)

    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()  # not sure if i need this
        return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def post_a_state():
    "post a new state"
    kwargs = request.get_json()

    if not kwargs:
        abort(400, 'Not a JSON')

    if 'name' not in kwargs:
        abort(400, 'Missing name')

    new_state = State(**kwargs)  # if this doesnt work, use json.load
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route(
    '/states/<string:state_id>',
    strict_slashes=False,
    methods=['PUT'])
def update_a_state(state_id):
    "update a state with put"

    state = storage.get("State", state_id)

    if not state:
        abort(404)

    new = request.get_json()
    if not new:
        abort(400, 'Not a JSON')

    for k, v in new.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)

    storage.save()

    return jsonify(state.to_dict()), 200
