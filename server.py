from flask import Flask, request, jsonify
from flask_cors import CORS
import nosyBird

# NosyBird Configuration
nosyBird.Configuration.set_credDB("accounts.db")
nosyBird.Configuration.set_tweetsJSON("tweets.JSON")
nosyBird.Configuration.set_credJSON("Credentials.JSON")

# Create a web app instance with Flask
nosyBird = Flask(__name__)
CORS(nosyBird)  # Enable CORS for all routes

# Normal Response
@nosyBird.route("/")
def index():
    return "200"

# POST request to write likes
@nosyBird.route("/username", methods=["POST"])
def saveUserLikes():
    if request.method == "POST":
        username = request.form["username"]
        try:
            import nosyBird
            nosyBird.postUser(username)
            return "Got Likes Successfully"
        except Exception as e:
            print(e)  # Log the exception for debugging
            return "Something went wrong on our side", 500
    else:
        return "Invalid request method", 405
    
# POST request to restart likes
@nosyBird.route("/restart_likes", methods=["POST"])
def restartLikes():
    if request.method == "POST":
        try:
            import nosyBird
            nosyBird.restartLikes()
            return "Restarted Likes Successfully"
        except Exception as e:
            print(e)
            return "Something went wrong on our side", 500
    else:
        return "Invalid request method", 405
    

# GET request to retrieve JSON data
@nosyBird.route("/get_json", methods=["GET"])
def getJson():
    if request.method == 'GET':
        try:
            import nosyBird
            return jsonify(nosyBird.getLikes())
        except Exception as e:
            print(e)
            return "Something went wrong on our side", 500
    else:
        return "Invalid request method", 405


#GET request to retrieve mixed JSON data
@nosyBird.route("/get_mix", methods=["GET"])
def getMixedJson():
    if request.method == 'GET':
        try:
            import nosyBird
            mixed_likes = nosyBird.getMixedLikes()
            return jsonify(mixed_likes)
        except Exception as e:
            print(e)
            return "Something went wrong on our side", 500
    else:
        return "Invalid request method", 405


nosyBird.run(debug=True)
# By defect it will run on port 5000
# `http://localhost:5000/`