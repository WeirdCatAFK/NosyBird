import asyncio, json, os, sqlite3
from twscrape import API, gather
from random import shuffle

class Configuration:
    _tweetsJSON_path = None
    _credJSON_path = None
    _credDB_path = None

    @classmethod
    def set_tweetsJSON(cls, path):
        cls._tweetsJSON_path = path

    @classmethod
    def get_tweetsJSON(cls):
        return str(cls._tweetsJSON_path)

    @classmethod
    def set_credJSON(cls, path):
        cls._credJSON_path = path

    @classmethod
    def get_credJSON(cls):
        return str(cls._credJSON_path)

    @classmethod
    def set_credDB(cls, path):
        cls._credDB_path = path

    @classmethod
    def get_credDB(cls):
        return str(cls._credDB_path)


def checkForAccount():
    credDB_path = Configuration.get_credDB()
    if os.path.isfile(credDB_path):
        with open(Configuration.get_credJSON(), "r") as credentialsJSON:
            credentials = json.load(credentialsJSON)

        connection = sqlite3.connect(credDB_path)
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


async def writeLikesInJSON(username: str):
    tweetsJSON_path = Configuration.get_tweetsJSON()
    credJSON_path = Configuration.get_credJSON()
    credDB_path = Configuration.get_credDB()
    
    # Preparation
    api = API()  # API instance
    
    # Add account if it doesn't exist, else create it in db
    if checkForAccount():
        await api.pool.login_all()
    else:
        with open(credJSON_path, "r") as credentialsJSON:
            credentials = json.load(credentialsJSON)  
        await api.pool.add_account(credentials["Username"], credentials["Password"], "Null", "Null")
        await api.pool.login_all()
        
    # Get user ID
    try:
        user = await api.user_by_login(username)
        userID = user.id
    except:
        print('There is no user with that account name')
        return None

    # Get likes from the user
    likes = await gather(api.liked_tweets(userID, limit=10))
    print("Gotten likes")

    # Create JSON for server requests
    outputJSON = {"user": [], "tweets": []}

    # Load current Tweets
    for tweet in likes:
        outputJSON["user"].append(username)
        outputJSON["tweets"].append(tweet.url)

    # Load previous tweets
    try:
        with open(tweetsJSON_path, "r") as file:
            previousTweets = json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        previousTweets = {"user": [], "tweets": []}

    # Merge current and previous tweets
    outputJSON["user"] += previousTweets.get("user", [])
    outputJSON["tweets"] += previousTweets.get("tweets", [])
    
    # Dump everything onto a JSON file
    with open(tweetsJSON_path, "w") as file:
        json.dump(outputJSON, file, indent=4)
    print("Dumped likes onto JSON")
        
### Server management methods
def restartLikes():
    tweetsJSON_path = Configuration.get_tweetsJSON()
    tweets = {"user": [], "tweets": []}
    with open(tweetsJSON_path, "w") as file:
        json.dump(tweets, file, indent=4)
        print("Erased tweets from JSON")

def postUser(user: str):
    asyncio.run(writeLikesInJSON(user))
    print('Done')

def getLikes():
    tweetsJSON_path = Configuration.get_tweetsJSON()
    with open(tweetsJSON_path, 'r') as JSON:
        tweets =json.load(JSON)        
    return tweets

def getMixedLikes():
    tweetsJSON_path = Configuration.get_tweetsJSON()
    with open(tweetsJSON_path, 'r') as JSON:
        data = json.load(JSON)
    pairs = list(zip(data["user"], data["tweets"]))
    shuffle(pairs)
    
    mixedUsers, mixedTweets = zip(*pairs)
    
    mixedData = {
        "user": list(mixedUsers),
        "tweets": list(mixedTweets)   
    }
        
    return mixedData
