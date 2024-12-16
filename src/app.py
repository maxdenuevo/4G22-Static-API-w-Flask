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
    return jsonify(members), 200

@app.route('/add_member', methods=['POST'])
def add_member():
    new_member = request.json
    member = jackson_family.add_member(new_member)
    if member is not None:
        members = jackson_family.get_all_members()
        response = {
            "new_added": member,
            "family": members
        }
        return jsonify(response), 200
    else:
        response = {
            "response": f"El miembro con el nombre {new_member['first_name']} ya existe",
        }
        return jsonify(response), 400

@app.route('/delete_member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if member is None:
        response = {
            "response": f"El miembro con el id {member_id} no existe",
        }
        return jsonify(response), 404
    else:
        response = {
            "done": True
        }
        return jsonify(response), 200   
    
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
