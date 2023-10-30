#!/usr/bin/python3
"""view for amenities linked with places"""
from flask import Blueprint, jsonify
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views

places_amenities_view = Blueprint('places_amenities_view', __name__)


@places_amenities_view.route('/places/<place_id>/amenities',
                             methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity using place id"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenities = place.amenities
    return jsonify([amenity.to_dict() for amenity in amenities])


@places_amenities_view.route('/places/<place_id>/amenities/<amenity_id>',
                             methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """delete amenity using place and amenity id"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity not in place.amenities:
        return jsonify({"error": "Not found"}), 404
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@places_amenities_view.route('/places/<place_id>/amenities/<amenity_id>',
                             methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """line amenity with place using amenity and place id"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    if amenity in place.amenities:
        return jsonify(amenity.to_dict()), 200
    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


app_views.register_blueprint(places_amenities_view)
