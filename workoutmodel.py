

from flask import Flask, request, jsonify

from datetime import datetime

import uuid


class Workout:
    def __init__(self, date, distance, calories_burned, duration, workout_name=None, heart_rate=None, max_elevation=None, route_name=None):
        self.id = str(uuid.uuid4())
        self.workout_name = workout_name
        self.distance = distance
        self.calories_burned = calories_burned
        self.duration = duration
        self.heart_rate = heart_rate
        self.max_elevation = max_elevation
        self.pace = self.calculate_pace()
        self.date = datetime.strptime(date, '%m-%d-%Y').date()
        self.route_name = route_name


    # Treat: fix data validation, convert any km/mi over time to standard minutes per mile
    def calculate_pace(self):
        if self.distance and self.duration:
            # Assuming duration is in minutes and distance in kilometers
            return self.duration / self.distance
        return None


    def to_dict(self):
        return {
            'id': self.id,
            'workoutName': self.workout_name,
            'distance': self.distance,
            'caloriesBurned': self.calories_burned,
            'duration': self.duration,
            'heartRate': self.heart_rate,
            'maxElevation': self.max_elevation,
            'pace': self.pace,
            'date': self.date.isoformat(),
            'routeName': self.route_name
        }
