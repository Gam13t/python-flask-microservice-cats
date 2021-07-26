import os
import functools
from flask import request, Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from model import Cat
from database import db_session
import config

app = Flask(__name__)





def validate_cat_token(function):
    @functools.wraps(function )
    def wrapper( **kwarg):
        cat = request.headers.get('CAT_TOKEN')
        if config.CAT_TOKEN == request.headers.get('CAT_TOKEN'):
            return function(**kwarg)

        return jsonify({
            "status": "error",
            "message": "Invalid token...",
            "cat": cat,
            "tok": config.CAT_TOKEN
        }), 401
    return wrapper

@app.route('/')
def index():
    return jsonify('API IS CURRENTY ONLINE')

@app.route('/cats', methods=['GET'])
@validate_cat_token
def get_cats():

    entities_list = []

    try:
        data = db_session.query(Cat).all()

    except(SQLAlchemyError, DBAPIError):

        return jsonify({
            'status': 'error',
            'message': 'Something went wrong...',
            'data': [],
        })

    for entity in data:
        entities_list.append({'id': entity.id, 'name': entity.name, 'breed': entity.breed, 'color': entity.color})

    return jsonify({
        'status': 'success',
        'message': 'All cat entities are represented',
        'data': entities_list,
    }), 200

@app.route('/cat/<cat_id>', methods=['GET'])
@validate_cat_token
def get_cat_by_id(cat_id):
    try:
        entity = db_session.query(Cat).filter(Cat.id == cat_id).first()
    except(SQLAlchemyError, DBAPIError):
        return jsonify({
            'status': 'error',
            'message': 'Something went wrong...',
            'data': []
        })

    if entity:
        return jsonify({
            'status': 'success',
            'message': 'Cat entity by id is represented',
            'data': {'id': entity.id, 'name': entity.name, 'breed': entity.breed, 'color': entity.color},
        }), 200
    return jsonify({
        'status': 'error',
        'message': 'Entity with this ID is missing',
    })

@app.route('/cat', methods=['POST'])
@validate_cat_token
def create_cat_entity():
    data = request.get_json()

    name = data.get('name')
    breed = data.get('breed')
    color = data.get('color')

    try:
        new_entity = Cat(name=name, breed=breed, color=color)
        db_session.add(new_entity)
        db_session.commit()
    except (SQLAlchemyError, DBAPIError):
        return jsonify({
            'status': 'error',
            'message': 'Some kind of error happened while adding to database...'
        })
    return jsonify({
        'status': 'success',
        'message': 'New cat was added to database...'
    }), 201

@app.route('/cat/{cat_id}', methods=['DELETE'])  # TODO: NEED TO BE FIXED(BACKLOG)
@validate_cat_token
def remove_cat_entity(cat_id):
    entity = db_session.query(Cat).filter(Cat.id == cat_id).first()
    try:
        entity.delete()
        entity.commit()
    except (SQLAlchemyError, DBAPIError):
        return jsonify({
            'status': 'error',
            'message': 'Some kind of error happened while deleting from database...',
        })
    return jsonify({
        'status': 'success',
        'message': 'Entity was deleted successful...',
    }), 201


if __name__ == '__main__':
    app.run( debug=True )
