import nosyBird

# Configuration for the paths
nosyBird.Configuration.set_credDB(
    "accounts.db"
)  # twscrape always uses this name to create its db, only modify this if you want to tamper fully with NosyBird, note that it will always be created onto root
nosyBird.Configuration.set_tweetsJSON(
    "tweets.JSON"
)  # A global outputFile that practically its a temporal DB for the server
nosyBird.Configuration.set_credJSON(
    "Credentials.JSON"
)  # You have to create this file with the twitter dummy account for the game to function


# Checks that your credentials are correct and if they are already on the DB
nosyBird.checkForAccount()

# Gets the likes of a user and saves the to a JSON, the name POST its indicative of how you could use it if you mounted it onto a server
nosyBird.postUser("WeirdCat_AFK")  # Follow me btw

# Returns the JSON as a Python dict , it doesnt change anything
nosyBirdJSON = nosyBird.getLikes()
for user, like in zip(nosyBirdJSON["user"], nosyBirdJSON["tweets"]):
    print(user, like)

# Returns a mixed JSON as a Python dict
nosyBirdJSON = nosyBird.getMixedLikes()
for user, like in zip(nosyBirdJSON["user"], nosyBirdJSON["tweets"]):
    print(user, like)


# Eliminates all the entries from the JSON so you can start over
nosyBird.restartJson()
