#!/usr/bin/python3
'''
defines the view for user objects
'''
from flask import Flask, Blueprint, jsonify, request
from models import storage
from models.user import User
from api.v1.views import app_views

user_view = Blueprint('user_view', __name__)


@user_view.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
    get all user objects
    '''
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@user_view.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''
    get user using user id
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@user_view.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''
    user delete using user id
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    user.delete()
    storage.save()
    return jsonify({}), 200


@user_view.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    create a user
    '''
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@user_view.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''
    update user using user id
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
