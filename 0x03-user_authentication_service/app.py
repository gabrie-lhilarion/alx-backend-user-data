#!/usr/bin/env python3
"""
app.py - A basic Flask application that returns a JSON response.

This script sets up a Flask web server with a single route ("/")
that returns a welcome message in JSON format.
"""

from flask import Flask, jsonify, request
from auth import Auth

# Instantiate the Auth object
AUTH = Auth()

# Initialize the Flask application
app = Flask(__name__)


@app.route("/", methods=["GET"])
def welcome():
    """
    Handle GET requests to the root URL ("/").

    Returns:
        A JSON response with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Handle POST requests to the /users endpoint to register a new user.

    Expects form data fields:
        - email (str): The email of the user to register.
        - password (str): The password of the user to register.

    Returns:
        JSON: A response indicating the result of the registration process.

    Possible Responses:
        - Success: {"email": "<registered email>", "message": "user created"}
        - Failure: {"message": "email already registered"}, status 400
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    """
    Run the Flask app on the local server.

    The app will be accessible on all network interfaces at port 5000.
    """
    app.run(host="0.0.0.0", port="5000")
