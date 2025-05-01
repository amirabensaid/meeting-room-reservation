from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from datetime import datetime, date
import os
import requests

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "default-dev-key")
jwt = JWTManager(app)

# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Custom Prometheus metrics
reservation_create_counter = Counter('reservation_create_requests', 'Total reservation creation attempts')
reservation_fetch_counter = Counter('reservation_fetch_requests', 'Total reservation fetch attempts')
reservation_cancel_counter = Counter('reservation_cancel_requests', 'Total reservation cancellation attempts')

def fetch_valid_room_ids():
    try:
        response = requests.get("http://room-service:5001/rooms", headers={"Authorization": request.headers.get("Authorization")})
        if response.status_code == 200:
            return [room["id"] for room in response.json()]
    except Exception as e:
        print("Room service unavailable:", e)
    return []


# In-memory reservation storage
reservations = [
    {
        "id": 1,
        "room_id": 1,
        "username": "user1",
        "date": "2025-04-30",
        "start_time": "09:00",
        "end_time": "10:00",
        "purpose": "Team Meeting"
    },
    {
        "id": 2,
        "room_id": 2,
        "username": "admin",
        "date": "2025-04-30",
        "start_time": "11:00",
        "end_time": "12:00",
        "purpose": "Client Call"
    }
]

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Reservation service is running"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations():
    reservation_fetch_counter.inc()
    username = get_jwt_identity()
    room_id = request.args.get('room_id')
    date_filter = request.args.get('date')

    filtered = reservations

    if room_id:
        filtered = [r for r in filtered if r['room_id'] == int(room_id)]
    if date_filter:
        filtered = [r for r in filtered if r['date'] == date_filter]

    if username != "admin":
        filtered = [r for r in filtered if r['username'] == username]

    return jsonify(filtered), 200

@app.route('/reservations/<int:reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    username = get_jwt_identity()
    for reservation in reservations:
        if reservation['id'] == reservation_id:
            if username != "admin" and reservation['username'] != username:
                return jsonify({"error": "Access denied"}), 403
            return jsonify(reservation), 200
    return jsonify({"error": "Reservation not found"}), 404

@app.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    reservation_create_counter.inc()
    username = get_jwt_identity()
    data = request.get_json()
    valid_room_ids = fetch_valid_room_ids()

    required = ["room_id", "date", "start_time", "end_time", "purpose"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    # Validate date
    try:
        res_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format, must be YYYY-MM-DD"}), 400

    if res_date < date.today():
        return jsonify({"error": "Cannot reserve a room in the past"}), 400

    # Validate time
    try:
        start_time = datetime.strptime(data["start_time"], "%H:%M").time()
        end_time = datetime.strptime(data["end_time"], "%H:%M").time()
    except ValueError:
        return jsonify({"error": "Invalid time format, must be HH:MM"}), 400

    if start_time >= end_time:
        return jsonify({"error": "End time must be after start time"}), 400

    # Validate room ID
    if data["room_id"] not in valid_room_ids:
        return jsonify({"error": "Room does not exist"}), 400

    # Check for time conflicts
    for reservation in reservations:
        if reservation["room_id"] == data["room_id"] and reservation["date"] == data["date"]:
            existing_start = datetime.strptime(reservation["start_time"], "%H:%M").time()
            existing_end = datetime.strptime(reservation["end_time"], "%H:%M").time()
            if start_time < existing_end and end_time > existing_start:
                return jsonify({"error": "Time slot already booked for this room"}), 409

    new_id = max((r["id"] for r in reservations), default=0) + 1
    new_reservation = {
        "id": new_id,
        "room_id": data["room_id"],
        "username": username,
        "date": data["date"],
        "start_time": data["start_time"],
        "end_time": data["end_time"],
        "purpose": data["purpose"]
    }

    reservations.append(new_reservation)
    return jsonify(new_reservation), 201

@app.route('/reservations/<int:reservation_id>', methods=['DELETE'])
@jwt_required()
def cancel_reservation(reservation_id):
    reservation_cancel_counter.inc()
    username = get_jwt_identity()
    for i, reservation in enumerate(reservations):
        if reservation['id'] == reservation_id:
            if username != "admin" and reservation['username'] != username:
                return jsonify({"error": "Access denied"}), 403
            del reservations[i]
            return jsonify({
                "message": "Reservation cancelled successfully",
                "reservation_id": reservation_id
            }), 200
    return jsonify({"error": "Reservation not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
