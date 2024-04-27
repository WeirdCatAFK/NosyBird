from flask import Flask, request, jsonify
from flask_cors import CORS
import nosyBird

# NosyBird Configuration
nosyBird.Configuration.set_credDB("accounts.db")
nosyBird.Configuration.set_tweetsJSON("tweets.JSON")
nosyBird.Configuration.set_credJSON("Credentials.JSON")

# Create a web app instance with Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Normal Response
@app.route("/")
def index():
    return "200"

# POST request to write likes
@app.route("/username", methods=["POST"])
def saveUserLikes():
    if request.method == "POST":
        data = request.json
        username = data.get("username")
        if username:
            try:
                import nosyBird
                nosyBird.postUser(username)
                return "Got Likes Successfully"
            except Exception as e:
                print(e)  # Log the exception for debugging
                return "Something went wrong on our side", 500
        else:
            return "Invalid request data", 400
    else:
        return "Invalid request method", 405
    
# POST request to restart likes
@app.route("/restart_likes", methods=["POST"])
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
@app.route("/get_mix", methods=["GET"])
def getMixedJson():
    if request.method == 'GET':
        try:
            mixed_likes = nosyBird.getMixedLikes()
            print(jsonify(mixed_likes))
            return jsonify(mixed_likes)
        except Exception as e:
            print(e)
            return "Something went wrong on our side", 500
    else:
        return "Invalid request method", 405


if __name__ == "__main__":
    app.run(debug=True)
    
    
# By default it starts on port 5000
# `http://localhost:5000/`
