from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from collections import defaultdict
import requests
import workoutmodel

app = Flask(__name__)
WEATHER_API_KEY = 'd370cd5b9a5c48d89b2164102240402'

workouts_db = [
  {
    "id": "e2fc7564-5d0e-435f-95a1-b9ef847d65c9",
    "workoutName": "Morning Run",
    "distance": 5.0,
    "caloriesBurned": 500,
    "duration": 30,
    "heartRate": 150,
    "maxElevation": 100,
    "pace": 6.0,
    "date": "2024-02-15",
    "routeName": "Park Loop"
  },
  {
    "id": "e2fc7564-5d0e-435f-95a1-b9ef847d65c9",
    "workoutName": "Morning Run",
    "distance": 5.5,
    "caloriesBurned": 520,
    "duration": 32,
    "heartRate": 152,
    "maxElevation": 105,
    "pace": 5.9,
    "date": "2024-02-22",
    "routeName": "River Trail"
  },
  {
    "id": "e2fc7564-5d0e-435f-95a1-b9ef847d65c9",
    "workoutName": "Morning Run",
    "distance": 6.0,
    "caloriesBurned": 540,
    "duration": 34,
    "heartRate": 154,
    "maxElevation": 110,
    "pace": 5.8,
    "date": "2024-02-29",
    "routeName": "Mountain Path"
  },
  {
    "id": "e2fc7564-5d0e-435f-95a1-b9ef847d65c9",
    "workoutName": "Morning Run",
    "distance": 6.5,
    "caloriesBurned": 560,
    "duration": 69,
    "heartRate": 156,
    "maxElevation": 115,
    "pace": 5.7,
    "date": "2024-03-07",
    "routeName": "City Run"
  },
  {
    "id": "e2fc7564-5d0e-435f-95a1-b9ef847d65c9",
    "workoutName": "Morning Run",
    "distance": 7.0,
    "caloriesBurned": 580,
    "duration": 10000000,
    "heartRate": 158,
    "maxElevation": 120,
    "pace": 5.6,
    "date": "2024-03-14",
    "routeName": "Beachside Track"
  }
]


@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/createworkout", methods=["POST"])
def createworkout():
    data = request.get_json()

    # Check for missing required fields
    required_fields = ['date', 'distance', 'calories_burned', 'duration']

    for field in required_fields: 
        if field not in data: 
            return jsonify({'error': 'Missing required workout data: ' + field}), 400

    image = data.get("image", "No image")

    # Create a Workout instance from the provided data
    workout = workoutmodel.Workout(
        date=data['date'],
        image=image,
        distance=data['distance'],
        calories_burned=data['calories_burned'],
        duration=data['duration'],
        workout_name=data.get('workoutName'),
        heart_rate=data.get('heartRate'),
        max_elevation=data.get('maxElevation'),
        route_name=data.get('routeName')
    )

    # Add the workout to the database (in this case, a list)
    workouts_db.append(workout.to_dict())
    print(workouts_db)
    return jsonify({'message': 'Workout record created successfully', 'id': workout.id}), 201

@app.route("/api/givemeworkout/<workout_id>", methods = ["GET"])
def giveWorkout(workout_id):
    
    workout = next((workout for workout in workouts_db if workout['id'] == workout_id), None)

    if workout is not None: 
        return jsonify(workout), 200
    else: 
        return jsonify({'error': 'Workout not found'}), 404


@app.route("/api/totaldistance/<timeframe>", methods=["GET"])
def total_distance(timeframe):
    distance_sums = defaultdict(float)
    
    for workout in workouts_db:
        date = datetime.strptime(workout['date'], '%Y-%m-%d').date()
        if timeframe == 'week':
            key = date.strftime('%Y-%U')  # Year and week number
        elif timeframe == 'month':
            key = date.strftime('%Y-%m')  # Year and month
        else:
            return jsonify({'error': 'Invalid timeframe specified'}), 400
        
        distance_sums[key] += workout['distance']
    
    return jsonify(dict(distance_sums)), 200

@app.route("/api/averageduration", methods=["GET"])
def average_duration():
    if not workouts_db:
        return jsonify({'error': 'No workout data available'}), 404
    
    total_duration = sum(workout['duration'] for workout in workouts_db)
    average_duration = total_duration / len(workouts_db)
    
    return jsonify({'averageDuration': average_duration}), 200

@app.route("/api/personal_bests/", methods=["GET"])
def personal_bests():
    # Retrieve user's personal bests

    if not workouts_db:
        return jsonify({'error': 'No workouts found for the given user'}), 404
    
    longest_distance = max(workouts_db, key=lambda x: x['distance'])
    
    longest_duration = max(workouts_db, key=lambda x: x['duration'])


    personal_bests = {
    'longestDistance': {
        'id': longest_distance['id'],
        'distance': longest_distance['distance'],
        'date': longest_distance['date']
    },
    'longestDuration': {
        'id': longest_duration['id'],
        'duration': longest_duration['duration'],
        'date': longest_duration['date']
        }
    }

    return jsonify(personal_bests), 200

def get_tomorrows_weather(location):
    url = f"http://api.weatherapi.com/v1/current.json?key=5338b0214a6541e7994165946240402&q={location}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@app.route('/api/weather/tomorrow/<location>', methods=['GET'])
def api_tomorrows_weather(location):
    weather_data = get_tomorrows_weather(location)
    
    if weather_data:
        # Here, you can customize what data to send back to your client
        # For simplicity, this example sends back the entire response
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Failed to retrieve weather data'}), 500



if __name__ == '__main__':
    app.run(debug=True)