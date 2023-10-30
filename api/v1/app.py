#!/usr/bin/python3
'''
This module starts a basic application.
'''
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, origins=["0.0.0.0"])


@app.teardown_appcontext
def teardown_appcontext(exception):
    '''
    This function closes the database connection.
    '''
    storage.close()

# Handler for 404 errors


@app.errorhandler(404)
def not_found(error):
    '''
    This function handles 404 errors and returns a JSON response.
    '''
    response = {
        "error": "Not found"
    }
    return jsonify(response), 404


if __name__ == '__main__':
    import os

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    app.run(host=host, port=port, threaded=True)
