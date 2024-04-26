from flask import Flask, request, jsonify
from nosyBird import restartJson, writeLikesInJSON


#Create a web app instance with Flask
nosyBird = Flask(__name__)

#Normal Responce
@nosyBird.route("/")
def index():
    return "200"

#Get request to write Likes 
@nosyBird.route("/json", methods = ["POST"])
def save_names():
    args = request.args
    
