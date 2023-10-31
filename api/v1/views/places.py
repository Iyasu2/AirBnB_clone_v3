#!/usr/bin/python3
'''
This module defines the view for Place objects.
'''
from flask import Flask, Blueprint, jsonify, request
from models import storage
from models.place import Place
from models.state import State
from models.city import City
from api.v1.views import app_views
from api.v1.views.cities import get_city


@app_views.route('/cities/<city_id>/places',
                  methods=['GET'], strict_slashes=False)
def get_places(city_id):
    '''
    get places from city id
    '''
    city = get_city(city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    places = storage.all(Place)
    city_places = [place.to_dict() for place in places.values()
                   if place.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    '''
    get place from place id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                  methods=['DELETE'],
                  strict_slashes=False)
def delete_place(place_id):
    '''
    delete place from place id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                  methods=['POST'], strict_slashes=False)
def create_place(city_id):
    '''
    create place inside city using city id
    '''
    city = get_city(city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    user_id = data["user_id"]
    user = storage.get(User, user_id)  # Make sure to import the User model
    if user is None:
        return jsonify({"error": "Not found"}), 404

    place = Place(city_id=city_id)
    for key, value in data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''
    update place from place id
    '''
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    keys_to_ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keys_to_ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])

    if not states and not cities:
        places = storage.all(Place).values()
    else:
        places = set()

        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state is not None:
                    for city in state.cities:
                        places.update(city.places)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city is not None:
                    places.update(city.places)

    if amenities:
        places = [
            place for place in places
            if all(amenity_id in place.amenities for amenity_id in amenities)
        ]

    place_dicts = [place.to_dict() for place in places]

    return jsonify(place_dicts)
