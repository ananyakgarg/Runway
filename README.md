
# Runway API

## Overview

This API was designed with the goal of providing users with a robust solution for tracking their fitness activities, specifically focusing on workouts. The API allows for creating workout records, retrieving specific workout information, aggregating total distances over time frames, calculating average workout durations, and identifying personal bests in distances and durations. This document outlines the design decisions, choice of tools, and instructions for running and testing the API, alongside considerations of trade-offs involved in its development.

## Design Decisions

### Simplified Data Model
The data model was intentionally kept simple, using a list to store workout records. This approach was chosen to focus on demonstrating API functionality without the complexity of integrating a database. However, for a production environment, it would be advisable to use a database system (e.g., PostgreSQL, MongoDB) to handle data persistence, scalability, and complex queries more efficiently.

### Use of Flask
Flask was chosen for its simplicity and flexibility as a micro web framework. It allows for quick setup and easy routing for API endpoints, making it ideal for small to medium projects and prototyping. Flask's extensive documentation and community support also contribute to its selection.

### Weather Integration
The API includes functionality to fetch weather data for a given location, showcasing how external APIs can be integrated to enrich the application's capabilities. This feature could be used to plan workouts based on weather conditions. The decision to include this demonstrates a real-world application scenario, though it introduces external dependencies.

### Data Validation
Basic data validation (e.g., checking for missing required fields) is implemented to ensure data integrity. However, this aspect could be expanded in a production environment with more comprehensive validation rules and error handling mechanisms to cover a wider range of potential issues.

## Choice of Tools

- **Python & Flask**: Chosen for their simplicity and effectiveness in building RESTful APIs.
- **WeatherAPI**: An external API used to demonstrate integrating third-party services for added functionality.

## Running the API

1. **Set Up Environment**:
    - Ensure Python 3.x is installed.
    - Install Flask: `pip install Flask`.
    - (Optional) Set up a virtual environment: `python -m venv venv`.

2. **Start the API**:
    - Navigate to the API directory.
    - Run `flask run` to start the server.
    - The API will be accessible at `http://127.0.0.1:5000/`.

## Testing the API

You can test the API using tools like Postman or curl. Here are examples for some of the endpoints:

- **Create Workout**:
  - POST `/api/createworkout` with a JSON body containing workout details.
- **Get Workout by ID**:
  - GET `/api/givemeworkout/<workout_id>`.
- **Get Total Distance**:
  - GET `/api/totaldistance/<timeframe>`, where `<timeframe>` can be `week` or `month`.
- **Get Average Duration**:
  - GET `/api/averageduration`.
- **Get Personal Bests**:
  - GET `/api/personal_bests/`.
- **Get Tomorrow's Weather for a Location**:
  - GET `/api/weather/tomorrow/<location>`.

## Trade-offs and Considerations

- **Simplicity vs. Scalability**: The current design favors simplicity for demonstration purposes. For scalability and production readiness, incorporating a database and considering an asynchronous framework like FastAPI for better performance might be beneficial.
- **Flexibility vs. Standardization**: The API allows for a flexible data model but lacks standardization in some areas (e.g., date formats). Implementing stricter data validation and adopting standards like ISO 8601 for dates could improve consistency and interoperability.
- **Feature Set**: The decision to include weather data demonstrates the potential for integrating external services. However, this introduces external dependencies and potential failure points, highlighting the trade-off between enriched features and reliability.

```
