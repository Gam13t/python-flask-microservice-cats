from flask import request, Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from model import Cat
from database import db_session

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify('API IS CURRENTY ONLINE')


@app.route('/cats', methods=['GET'])
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


@app.route('/cat/{cat_id}', methods=['DELETE'])
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
    app.run()
