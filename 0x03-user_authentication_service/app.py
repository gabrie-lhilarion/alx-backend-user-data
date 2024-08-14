#!/usr/bin/env python3
"""
app.py - A basic Flask application that returns a JSON response.

This script sets up a Flask web server with a single route ("/")
that returns a welcome message in JSON format.
"""

from flask import Flask, jsonify

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

if __name__ == "__main__":
    """
    Run the Flask app on the local server.
    
    The app will be accessible on all network interfaces at port 5000.
    """
    app.run(host="0.0.0.0", port="5000")
