from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
import os
from bson import json_util

app = Flask(__name__)


# app.config['MONGO_URI'] = "mongodb+srv://raghavintern:<patiala1034>@cluster0.cucbwel.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(os.environ.get('MONGO_URI'))
db = client['user']
user_collection = db['Students']



@app.route('/users', methods=['GET'])
def get_all_users():
    users = list(user_collection.find())
    return json_util.dumps({'users': users})


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = user_collection.find_one({'_id': ObjectId(id)})
    if user:
        return json_util.dumps({'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    new_user = {
        'name': request.json['name'],
        'marks': request.json['marks'],
        'roll_number': request.json['roll_number'],
        'address': request.json['address']
    }
    result = user_collection.insert_one(new_user)
    return jsonify({'id': str(result.inserted_id)})


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = user_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 1:
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404




@app.route('/users/<id>', methods=['PATCH'])
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
