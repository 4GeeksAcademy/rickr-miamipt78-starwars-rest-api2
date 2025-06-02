"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Person, User_Person_Favorites
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

#user routes
@api.route('/users', methods=['GET'])
def get_users():
    
    # query the database to get all the starwars characters
    all_users = User.query.all()

    # take into consideration that there may be None records in the table
    if all_users is None:
        return jsonify('Sorry! No users found!'), 404
    else:
        all_users = list(map(lambda x: x.serialize(), all_users))
        return jsonify(all_users), 200


@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    
    user = db.session.get(User, user_id)
    all_people = [each_person.serialize() for each_person in user.favorite_people]
    # need to also get all favorite planets by user
    # then join both lists into a serializable object to send as a response
    
    if user is None:
        raise APIException(f'User ID {user.id} was not found!', status_code=404)
    else:
        return jsonify(all_people), 200
    


# profile routes
@api.route('/people', methods=['GET'])
def get_people():
    
    # query the database to get all the starwars characters
    all_people = Person.query.all()

    # take into consideration that there may be None records in the table
    if all_people is None:
        return jsonify('Sorry! No Star Wars characters found!'), 404
    else:
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200


@api.route('/people/<int:person_id>', methods=['GET'])
def get_single_person(person_id):
    
    # query the database to get a SPECIFIC starwars character by id
    single_person = db.session.get(Person, person_id)

    if single_person is None:
        raise APIException(f'Person ID {person_id} was not found!', status_code=404)

    single_person = single_person.serialize()
    return jsonify(single_person), 200


@api.route('/planets', methods=['GET'])
def get_planets():
    pass

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    pass

