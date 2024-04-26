import asyncio, json, os, sqlite3
from twscrape import API, gather


def checkForAccount(dbPath):
    if os.path.isfile(dbPath):
        with open("Credentials.JSON", "r") as credentialsJSON:
            credentials = json.load(credentialsJSON)

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

def postUser(user: str, tweetsJSON_path: str, credJSON_path: str, credDB_path: str):
    asyncio.run(writeLikesInJSON(user,tweetsJSON_path,credJSON_path, credDB_path))
    print('Done')


async def writeLikesInJSON(
    username: str,
    tweetsJSON_path: str,
    credJSON_path: str,
    credDB_path: str,
):
    # Preparation
    api = API()  # API instance
    
    # Add account if it doesn't exist, else create it in db
    if checkForAccount(credDB_path):
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
        
