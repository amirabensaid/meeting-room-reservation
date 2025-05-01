from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from werkzeug.security import generate_password_hash, check_password_hash
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default-dev-key")
jwt = JWTManager(app)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Custom Prometheus metrics
login_counter = Counter('user_login_requests', 'Total number of user login attempts')
user_fetch_counter = Counter('user_fetch_requests', 'Total number of user fetch attempts')
role_check_counter = Counter('role_check_requests', 'Total number of role check attempts')

# In-memory database for users (to be replaced with a real database in production)
users = {
    "admin": {"password": generate_password_hash("admin123"), "role": "admin"},
    "user1": {"password": generate_password_hash("pass123"), "role": "user"},
    "user2": {"password": generate_password_hash("pass456"), "role": "user"}
}

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "User service is running"}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint to check if the service is running"""
    return jsonify({"status": "healthy"}), 200

@app.route('/login', methods=['POST'])
def login():
    login_counter.inc()  # Increment on each login attempt
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data.get('username')
    password = data.get('password')

    # Validate user credentials
    if username not in users or not check_password_hash(users[username]["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Create access token using Flask-JWT-Extended
    access_token = create_access_token(identity=username)

    return jsonify({
        "access_token": access_token,
        "username": username,
        "role": users[username]["role"]
    }), 200

@app.route('/users/me', methods=['GET'])
@jwt_required()
def get_user_info():
    """Endpoint to get current user information"""
    current_user = get_jwt_identity()

    if current_user not in users:
        return jsonify({"error": "User not found"}), 404

    # Don't return the password
    user_info = {
        "username": current_user,
        "role": users[current_user]["role"]
    }

    return jsonify(user_info), 200

@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    user_fetch_counter.inc()  # Increment when fetching user list
    current_user = get_jwt_identity()

    # Check if user is admin
    if users[current_user]["role"] != "admin":
        return jsonify({"error": "Access denied. Admin role required."}), 403

    # Return all users (without passwords)
    user_list = [{"username": username, "role": details["role"]} for username, details in users.items()]

    return jsonify(user_list), 200

@app.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()

    # Check if user is admin
    if users[current_user]["role"] != "admin":
        return jsonify({"error": "Access denied. Admin role required."}), 403

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    username = data["username"]
    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    # Create user
    users[username] = {
        "password": generate_password_hash(data["password"]),
        "role": data["role"]
    }

    return jsonify({"message": f"User {username} created successfully"}), 201

@app.route('/users/role/<username>', methods=['GET'])
@jwt_required()
def check_user_role(username):
    """Endpoint to check if a user has a specific role."""
    role_check_counter.inc()  # Increment on each role check request
    current_user = get_jwt_identity()

    # Ensure the requesting user is an admin before allowing role check
    if users[current_user]["role"] != "admin":
        return jsonify({"error": "Access denied. Admin role required."}), 403

    if username not in users:
        return jsonify({"error": "User not found"}), 404

    # Return the user's role
    return jsonify({"username": username, "role": users[username]["role"]}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
