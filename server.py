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

if __name__ == "__main__":
    nosyBird.run(debug=True)
