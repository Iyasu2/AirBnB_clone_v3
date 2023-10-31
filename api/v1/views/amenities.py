#!/usr/bin/python3
'''
module defines the view for Amenity objects.
'''
from flask import Blueprint, jsonify, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views

amenity_view = Blueprint('amenity_view', __name__)


@amenity_view.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''
    get all amenities
    '''
    amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in amenities.values()])


@amenity_view.route('/amenities/<amenity_id>',
                    methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    '''
    get amenities from amenity id
    '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())


@amenity_view.route('/amenities/<amenity_id>',
                    methods=['DELETE'],
                    strict_slashes=False)
def delete_amenity(amenity_id):
    '''
    delete amenity by amenity id
    '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@amenity_view.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    '''
    create amenity object
    '''
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@amenity_view.route('/amenities/<amenity_id>',
                    methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    '''
    update amenity object by amenity id
    '''
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
