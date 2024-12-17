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

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"message": f"Member with id {member_id} not found"}), 400
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    if not request.json:
        return jsonify({"message": "Invalid request body"}), 400
    
    new_member = request.json
    required_fields = ['first_name', 'age', 'lucky_numbers']
    
    if not all(field in new_member for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400
        
    member = jackson_family.add_member(new_member)
    if member is None:
        return jsonify({"message": f"Member with name {new_member['first_name']} already exists"}), 400
    
    return jsonify(member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    member = jackson_family.delete_member(member_id)
    if member is None:
        return jsonify({"message": f"Member with id {member_id} not found"}), 400
    
    return jsonify({"done": True}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
