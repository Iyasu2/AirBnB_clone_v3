#!/usr/bin/python3
'''
module defines the view for City objects.
'''
from flask import Blueprint, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views

city_view = Blueprint('city_view', __name__)


@city_view.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    '''
    get city object by state_id
    '''
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    cities = state.cities
    return jsonify([city.to_dict() for city in cities])


@city_view.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''
    get city object by city id
    '''
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())


@city_view.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''
    delete city object by city id
    '''
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    city.delete()
    storage.save()
    return jsonify({}), 200


@city_view.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''
    create city in state by state id
    '''
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    city = City()
    for key, value in data.items():
        setattr(city, key, value)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@city_view.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''
    update city by city id
    '''
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200


'''
Register the state_view Blueprint under app_views
'''
app_views.register_blueprint(city_view)
