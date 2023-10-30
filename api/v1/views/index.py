#!/usr/bin/python3
'''
this returns status of API
'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status_api():
    '''
    returns status of api
    '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats_api():
    '''
    returns number of each type of class
    '''
    stats = {
            'amenities': storage.count('Amenity'),
            'cities': storage.count('City'),
            'places': storage.count('Place'),
            'reviews': storage.count('Review'),
            'states': storage.count('State'),
            'users': storage.count('User')
            }

    return jsonify(stats)
