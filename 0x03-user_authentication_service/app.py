#!/usr/bin/env python3
"""
app.py - A basic Flask application that returns a JSON response.

This script sets up a Flask web server with a single route ("/")
that returns a welcome message in JSON format.
"""

from flask import Flask, jsonify, request, abort
from flask import make_response, redirect, url_for
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


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """
    Handle profile retrieval for a logged-in user.

    This route expects the session ID to be provided as a cookie.
    If the session is valid, it returns the user's email.
    If the session is invalid, a 403 status code is returned.

    Returns:
        str: A JSON response with the user's email or a 403 error.
    """
    # Retrieve the session ID from cookies
    session_id = request.cookies.get('session_id')

    # If session ID is missing or invalid, respond with a 403 status code
    if not session_id:
        abort(403)

    # Find the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    # Return the user's email with a 200 status
    return jsonify({"email": user.email})


@app.route("/sessions", methods=["DELETE"])
def logout() -> None:
    """
    Handle user logout by destroying the session.

    This route expects the session ID to be provided as a cookie.
    If the session is valid, it will be destroyed and the user
    will be redirected to the home page. If the session is invalid,
    a 403 status code is returned.

    Returns:
        None
    """
    # Retrieve the session ID from cookies
    session_id = request.cookies.get('session_id')

    # If session ID is missing or invalid, respond with a 403 status code
    if not session_id:
        abort(403)

    # Find the user associated with the session ID
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    # Destroy the user's session
    AUTH.destroy_session(user.id)

    # Redirect the user to the home page
    return redirect(url_for("index"))


@app.route("/", methods=["GET"])
def index() -> str:
    """
    Home route that welcomes the user.

    Returns:
        str: A simple welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    POST /reset_password route to generate a password reset token.

    Expects form data with an "email" field.
    If the email is not registered, responds with a 403 status code.
    Otherwise, generates a reset token and responds with a 200 status code
    and a JSON payload containing the email and reset token.

    Returns:
        Response: JSON response with the email and reset token or an error.
    """
    # Get the email from the form data
    email = request.form.get('email')
    if not email:
        abort(400, description="Email is required")

    try:
        # Generate the reset token
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        # If the email is not registered, respond with a 403 status code
        abort(403)

    # Return the JSON response with the email and reset token
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    Update password endpoint to handle PUT /reset_password requests.

    Expects form data with 'email', 'reset_token', and 'new_password'.

    Returns:
        - 200 HTTP status and a JSON payload on success.
        - 403 HTTP status if the reset token is invalid.
    """
    # Extract form data from the request
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    # Validate required fields
    if not email or not reset_token or not new_password:
        return jsonify({"message": "Missing fields"}), 403

    try:
        # Update the password
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # If the reset token is invalid, return 403 status code
        return jsonify({"message": "Invalid reset token"}), 403

    # Respond with success if password is updated
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    """
    Run the Flask app on the local server.

    The app will be accessible on all network interfaces at port 5000.
    """
    app.run(host="0.0.0.0", port="5000")
