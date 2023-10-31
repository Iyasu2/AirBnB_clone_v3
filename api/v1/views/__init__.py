#!/usr/bin/python3
'''
this is the initialization module
'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *

app_views.register_blueprint(states.state_view)
app_views.register_blueprint(cities.city_view)
app_views.register_blueprint(amenities.amenity_view)
app_views.register_blueprint(users.user_view)
app_views.register_blueprint(places.place_view)
app_views.register_blueprint(places_reviews.places_reviews_view)
app_views.register_blueprint(places_amenities.places_amenities_view)
