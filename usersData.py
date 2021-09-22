
import json
from bson.json_util import dumps
from config import client
from app import app
from flask import request, jsonify, make_response
import random

import ast

db = client.restfulapi

collection = db.users



@app.route("/")
def get_initial_response():
    message = {
        'apiversion': 'v1.0',
        'status': '200',
        'message': 'welcome to flask API'
    }

    resp = jsonify(message)

    return resp

# Creating Account with new User
@app.route("/api/v1/new_user", methods=['POST'])
def new_user():
    data = dumps(request.get_json())
    my_data = json.loads(data)
    account_no = random.randomint(10000, 99999)
    my_data["account_number"] = account_no
    collection.insert_many(my_data)
    return make_response(jsonify({"msg": "Data inserted successfully"}), 201),
# return make_response(jsonify({"msg": "invalid Data"}), 400)

# Displaying All Users
@app.route("/api/v1/getalluser",methods = ["GET"])
def all_users():
    user_data = collection.find({}, {"_id": 0})
    if user_data.count() > 0:
        response = dumps([data for data in user_data])
        return make_response(jsonify({"msg":"Bank Users List"}), 200)

    return make_response(jsonify({"msg":"User not Found"}), 400)


# Displaying Particular User

@app.route("/api/v1/getuser",methods = ["GET"])
def getuser():
    first_name = request.args.get('fname')
    last_name = request.args.get('lname')
    full_name = " ".join(first_name, last_name)

    input_data = collection.find({"name": full_name}, {"_id": 0})



    if input_data.count() > 0 :
        response = dumps(input_data)
        return response, 200

    return make_response(jsonify({"msg": "User not Found"}), 400)


# Updating User Record
@app.route("/api/v1/updateuser/<account_no>", methods=['PUT'])
def update_user(account_no):
    update_user_data = request.get_json()
    data = collection.find_one({'account_number': account_no})
    if data:
        collection.update_one({'account_number': account_no}, {"$set": update_user_data})
        return make_response(jsonify({"msg": "User updated.."}), 200)
    return make_response(jsonify({"msg": "User not found"}), 404)



# Deleting User Account
@app.route("/api/v1/deleteuser/<account_no>", methods=['DELETE'])

def delete_user(account_no):
    data = collection.find_one({'account_number': account_no})
    if data:
        collection.delete_many({"account_number": account_no})
        return make_response(jsonify({"msg": "User deleted..."}), 200)
    return make_response(jsonify({"msg": "User not found"}), 404)
