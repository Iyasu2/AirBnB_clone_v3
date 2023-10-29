#!/usr/bin/python3
'''
This module defines the view for User objects.
'''
from flask import Flask, Blueprint, jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views

user_view = Blueprint('user_view', __name__)


@user_view.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''
    get all users
    '''
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


@user_view.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''
    get user by user id
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


@user_view.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    '''
    delete user by user id
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    user.delete()
    storage.save()
    return jsonify({})


@user_view.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    create a user object
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
    update user by user id
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


'''
Register the state_view Blueprint under app_views
'''
app_views.register_blueprint(user_view)
