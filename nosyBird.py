import asyncio, json, os, sqlite3
from twscrape import API, gather


def checkForAccount(dbPath):
    if os.path.isfile(dbPath):
        with open("Credentials.JSON", "r") as credentialsJSON:
            credentials = json.loads(credentialsJSON)

        connection = sqlite3.connect(dbPath)
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT username, password \r\nFROM accounts \r\nWHERE username LIKE '{credentials["Username"]}' \r\nAND password LIKE '{credentials["Password"]}';\r\n"
        )
        if cursor.fetchall():
            print("Account found...")
            return True
        else:
            print("Account not found")
            return False
    else:
        print("There was not a DB instance...")
        return False

def restartJson(tweetsJSON_path):
    tweets = {"user": [], "tweets": []}
    with open(tweetsJSON_path, "w") as file:
        json.dump(tweets, file, indent=4)
        print("Errased")

async def writeLikesInJSON(
    username: str,
    tweetsJSON_path: str = "tweets.JSON",
    credJSON_path: str = "Credentials.JSON",
    credDB_path: str = "accounts.db",
    
):
    # Preparation
    api = API()  # API instance
    # Add account if it doesnt exist, else create it in db
    if checkForAccount(credDB_path):
        api.pool.login_all()
    else:
        with open(credJSON_path, "r") as credentialsJSON:
            credentials = json.loads(credentialsJSON)        
        api.pool.add_account(credentials["Username"], credentials["Password"])
        api.pool.login_all()
    #Get user ID
    user = await api.user_by_login(username)
    userID = user.id
    
    #Get likes from the user
    likes = await gather(api.liked_tweets(username, limit = 10))
    
    #Create JSON for server requests
    outputJSON = {"user":[],"tweets":[]}
    
    #Load current Tweets
    for tweet in likes:
        outputJSON["user"].append(username)
        outputJSON["tweets"].append(tweet)
       
    #Load previous tweets 
    with open(tweetsJSON_path, "r") as file:
        previousTweets = json.load(file)
        if previousTweets:
            outputJSON["user"] = outputJSON["user"] + previousTweets["user"]
            outputJSON["tweets"] = outputJSON["tweets"] + previousTweets["tweets"]
    
    #Dump everything onto a JSON file
    with open(tweetsJSON_path, "w") as file:
        json.dump(outputJSON, file, indent=4)

    
    
    
    
        
