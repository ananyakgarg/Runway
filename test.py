from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict

import workoutmodel

app = Flask(__name__)

workouts_db = []

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/createworkout", methods=["POST"])
def createworkout():
    data = request.get_json()

    # Check for missing required fields
    required_fields = ['date', 'distance', 'caloriesBurned', 'duration', 'image']
    if any(field not in data for field in required_fields): 
        return jsonify({'error': 'Missing required workout data'}), 400

    image = data.get("image")

    # Create a Workout instance from the provided data
    workout = workoutmodel.Workout(
        date=data['date'],
        image=image,
        distance=data['distance'],
        calories_burned=data['caloriesBurned'],
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

@app.route("/api/personal_bests/<user_id>", methods=["GET"])
def personal_bests(user_id):
    # Retrieve user's personal bests
    pass

@app.route("/api/routes/recommendations", methods=["GET"])
def route_recommendations():
    # Suggest routes based on user history and preferences
    pass


if __name__ == '__main__':
    app.run(debug=True)