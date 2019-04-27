from flask import Flask, request, jsonify
import json
from bson.json_util import dumps
from pymongo import MongoClient
import math
from bson.objectid import ObjectId

app = Flask(__name__)


client = MongoClient('mongodb://localhost:27017/testing')
db = client.testing


##add contact to table 
@app.route("/add_contact", methods = ['POST'])
def add_contact():
    try:
        #decode data into json 
        data = json.loads(request.data) 
        user_name = data['name']
        user_age = data['age']
        user_phone_list = data['phone_list']
        if user_name and user_age and user_phone_list:
            status = db.person.insert_one({
                "name" : user_name,
                "age" : user_age,
                "phone_list" : user_phone_list
            })

        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})

##list all contact from table 
@app.route("/get_all_contact", methods = ['GET'])
def get_all_contact():
    try:
        contacts = db.person.find()
        return dumps({"data": contacts})
    except Exception as e:
        return dumps({'error' : str(e)})

    
# ##list contact find by name
@app.route("/get_by_name/<name>", methods = ['GET'])
def get_by_name(name):
    try:
        print("---> name: ", name)
        contacts = db.person.find_one({'name': str(name)})
        return dumps({"data": contacts})

    except Exception as e: 
        return dumps({'error' : str(e)})

##update contact by name 
@app.route("/update_name", methods = ['PUT'])
def update_name(): 
    try: 
        
        old_name = request.args.get("old_name")
        data = json.loads(request.data) 
        new_name = data['name']
  
        db.person.update_one({"name": old_name},{"$set": {"name": new_name}})
       

        return dumps({'message' : 'SUCCESS'})

    except Exception as e:
        return dumps({'error' : str(e)})


##delete data by name 
@app.route("/delete/<name>", methods = ['DELETE'])
def delete_by_name(name):
    try:
        contacts = db.person.delete_one({'name':name})
        return dumps({'message' : 'SUCCESS'})

    except Exception as a:
        return dumps({'error':str(a)})

if __name__ == '__main__':
  app.run(debug=True)