#!/usr/bin/python3
"""view for review"""
from flask import Blueprint, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """get review from place id"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """get review from review id"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete review from review id"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create review object"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user_id = data["user_id"]
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    if "text" not in data:
        return jsonify({"error": "Missing text"}), 400
    review = Review(place_id=place_id)
    for key, value in data.items():
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update review of review id"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in [
            'id',
            'user_id',
            'place_id',
            'created_at',
                'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
