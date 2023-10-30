#!/usr/bin/python3

"""
This module defines the view for User objects.
"""

from flask import Flask, Blueprint, jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views

user_view = Blueprint('user_view', __name__)


def get_users():
    '''
    Get a list of all users.
    Returns:
        JSON response with a list of user dictionaries.
    '''
    users = storage.all(User)
    return jsonify([user.to_dict() for user in users.values()])


def get_user(user_id):
    '''
    Get a user by user id.
    Args:
        user_id (str): The user's ID.
    Returns:
        JSON response with the user's dictionary.
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())


def delete_user(user_id):
    '''
    Delete a user by user id.
    Args:
        user_id (str): The user's ID.
    Returns:
        JSON response with an empty dictionary.
    '''
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    user.delete()
    storage.save()
    return jsonify({})


def create_user():
    '''
    Create a user object.
    Returns:
        JSON response with the created user's dictionary.
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


def update_user(user_id):
    '''
    Update a user by user id.
    Args:
        user_id (str): The user's ID.
    Returns:
        JSON response with the updated user's dictionary.
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
Register the user_view Blueprint under app_views
'''
app_views.register_blueprint(user_view)
