from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default-dev-key")
jwt = JWTManager(app)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Custom Prometheus metrics
get_rooms_counter = Counter('room_get_requests', 'Total number of room retrieval requests')
create_room_counter = Counter('room_create_requests', 'Total number of room creation requests')

# Mock database for rooms (to be replaced with a real database in production)
rooms = [
    {
        "id": 1,
        "name": "Conference Room A",
        "capacity": 10,
        "location": "1st Floor",
        "equipment": ["Projector", "Whiteboard"]
    },
    {
        "id": 2,
        "name": "Meeting Room B",
        "capacity": 6,
        "location": "2nd Floor",
        "equipment": ["TV Screen", "Whiteboard"]
    },
    {
        "id": 3,
        "name": "Board Room",
        "capacity": 20,
        "location": "3rd Floor",
        "equipment": ["Projector", "Video Conference System", "Whiteboard"]
    }
]

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Room service is running"}), 200


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint to check if the service is running"""
    return jsonify({"status": "healthy"}), 200

@app.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    """Endpoint to get all rooms"""
    get_rooms_counter.inc()  # Increment the counter when fetching rooms
    return jsonify(rooms), 200

@app.route('/rooms/<int:room_id>', methods=['GET'])
@jwt_required()
def get_room(room_id):
    """Endpoint to get a specific room by ID"""
    for room in rooms:
        if room['id'] == room_id:
            return jsonify(room), 200
    
    return jsonify({"error": "Room not found"}), 404

@app.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    """Endpoint to create a new room (admin only)"""
    create_room_counter.inc()  # Increment the counter when creating a room
    current_user = get_jwt_identity()

    # For simplicity, assume the role 'admin' is required to create a room
    if current_user != "admin":  # Replace this with real admin role checking
        return jsonify({"error": "Access denied. Admin role required."}), 403

    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ["name", "capacity", "location"]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Generate new room ID
    new_id = max(room["id"] for room in rooms) + 1 if rooms else 1
    
    # Create new room
    new_room = {
        "id": new_id,
        "name": data["name"],
        "capacity": data["capacity"],
        "location": data["location"],
        "equipment": data.get("equipment", [])
    }
    
    rooms.append(new_room)
    
    return jsonify(new_room), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
