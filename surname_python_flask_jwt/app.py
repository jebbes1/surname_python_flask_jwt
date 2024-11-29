from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "your_secret_key" 
jwt = JWTManager(app)

users = {} 
tokens = []  

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = password
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if users.get(username) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    tokens.append(access_token)  
    return jsonify({"access_token": access_token}), 200

@app.route('/set-jwt', methods=['POST'])
def set_jwt():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    access_token = create_access_token(identity={"message": message})
    tokens.append(access_token)  
    return jsonify({"jwt": access_token}), 200

@app.route('/get-jwt', methods=['GET'])
@jwt_required()
def get_jwt():
    current_user = get_jwt_identity()
    return jsonify({"current_user": current_user}), 200

if __name__ == '__main__':
    app.run(debug=True)
