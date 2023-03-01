from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from bson import json_util
from bson.errors import InvalidId
from models.classes import User
app = Flask(__name__)


client = MongoClient(os.environ.get('MONGO_URI'))
db = client['user']
user_collection = db['Students']


@app.errorhandler(InvalidId)
def handle_invalid_id(error):
    response = jsonify({'error': 'Given id is not a valid objectid'})
    response.status_code = 404
    return response


@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(user_collection.find())
    return json_util.dumps({'users': users})


@app.route('/users/<id>', methods=['GET'])
def get_user_by_id(id):
    try:
        user = user_collection.find_one({'_id': ObjectId(id)})
        if user is None:
            return json_util.dumps({'error': 'User not found'})
        return json_util.dumps({'user': user})
    except InvalidId:
        return handle_invalid_id(InvalidId())


@app.route('/users', methods=['POST'])
def create_user():
    try:
        user = User.from_dict(request.json)
    except (ValueError, TypeError) as e:
        return jsonify({'error': str(e)}), 400

    result = user_collection.insert_one(user.to_dict())
    return jsonify({'id': str(result.inserted_id)})


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        result = user_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'User deleted successfully'})
        return json_util.dumps({'error': 'User not found'})
    except InvalidId:
        return handle_invalid_id(InvalidId())


@app.route('/users/<id>', methods=['PUT'])
def update_user_roll_number(id):
    result = user_collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': {'roll_number': request.json['roll_number']}}
    )
    if result.modified_count == 1:
        return jsonify({'message': 'Roll number updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)



