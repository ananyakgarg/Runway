from flask import Flask, request, jsonify

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
    return jsonify({'message': 'Workout record created successfully', 'id': workout.id}), 201

@app.route("/api/givemeworkout/<workout_id>", methods = ["GET"])
def giveWorkout(workout_id):
    
    workout = next((workout for workout in workouts_db if workout['id'] == workout_id), None)

    if workout is not None: 
        return jsonify(workout), 200
    else: 
        return jsonify({'error': 'Workout not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)