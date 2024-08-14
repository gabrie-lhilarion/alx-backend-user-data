#!/usr/bin/env python3
"""
app.py - A basic Flask application that returns a JSON response.

This script sets up a Flask web server with a single route ("/")
that returns a welcome message in JSON format.
"""

from flask import Flask, jsonify, request, abort, make_response
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


@app.route('/sessions', methods=['POST'])
def login():
    """
    Handle user login and create a new session.

    Expected form data:
        - email: The user's email address.
        - password: The user's password.

    Returns:
        JSON response containing the user's email and a success message,
        and sets a session ID cookie if login is successful.
        Responds with 401 status if login fails.
    """
    # Extract form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate the credentials
    if not AUTH.valid_login(email, password):
        # Abort with a 401 status if login is invalid
        abort(401)

    # Create a session if login is valid
    session_id = AUTH.create_session(email)

    # Prepare the response with the session ID set as a cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    """
    Run the Flask app on the local server.

    The app will be accessible on all network interfaces at port 5000.
    """
    app.run(host="0.0.0.0", port="5000")
