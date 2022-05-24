"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():   
    members = jackson_family.get_all_members()
    if members is None:
        return jsonify ("Server error"),500
    elif members == False:
        return jsonify("Members do not exist"),400
    else:
        return jsonify(members), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):    
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify ("Server error"),500
    elif member == False:
        return jsonify("Member does not exist"),400
    else:
        return jsonify(member), 200

@app.route('/member/', methods=['POST'])
def add_member():    
    body=request.get_json()
    print (body)
    member = jackson_family.add_member(body)
    if member is None:
        return jsonify ("Server error"),500
    elif member == False:
        return jsonify("Member does not exist"),400
    else:
        return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):    
    member = jackson_family.delete_member(id)
    if member is None:
        return jsonify ("Server error"),500
    elif member == False:
        return jsonify("Member does not exist"),400
    else:
        return jsonify(member), 200




if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
