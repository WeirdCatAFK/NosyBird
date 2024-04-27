document.addEventListener('DOMContentLoaded', function () {
    // Array to store the list of players
    let players = [];
    var tweetContainer = document.getElementById('tweet-container');

    // Function to send a POST request to save user likes
    function saveUserLikes(username) {
        fetch('http://localhost:5000/username', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Something went wrong on the server');
                }
                return response.text();
            })
            .then(data => {
                console.log(data); // Log success message
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Function to send a POST request to restart likes
    function restartLikes() {
        fetch('http://localhost:5000/restart_likes', {
            method: 'POST'
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Something went wrong on the server');
                }
                return response.text();
            })
            .then(data => {
                console.log(data); // Log success message
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Function to fetch mixed JSON data from the server
    function getMixedJson() {
        return fetch('http://localhost:5000/get_mix')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Something went wrong on the server');
                }
                return response.json(); // Parse JSON response and return it
            })
            .then(data => {
                console.log(data); // Log retrieved JSON data
                return data; // Return the parsed JSON data
            })
            .catch(error => {
                console.error('Error:', error);
                throw error; // Re-throw the error to propagate it to the caller
            });
    }

    // Function to add a new user
    function addUser() {
        // Get the value entered by the user
        const userInput = document.getElementById('userInput').value.trim();

        // Check if the user input is not empty
        if (userInput !== '') {
            players.push(userInput);

            // Create a new user element
            const newUser = document.createElement('div');
            newUser.className = 'user';
            newUser.textContent = userInput;

            // Create a button to remove the user
            const removeButton = document.createElement('button');
            removeButton.className = 'removePlayer';
            removeButton.textContent = 'Remove Player';
            removeButton.addEventListener('click', function () {
                // Remove the user from the array
                const index = players.indexOf(userInput);
                if (index !== -1) {
                    players.splice(index, 1);
                }
                // Remove the user element from the DOM
                newUser.remove();
            });

            // Append the user element and remove button to the list
            newUser.appendChild(removeButton);
            document.getElementById('usersAlreadyPlaying').appendChild(newUser);

            // Clear the input field
            document.getElementById('userInput').value = '';
        }
    }
    // Function to get a tweet id from its url
    function getTweetIDFromURL(url) {
        var tweetID;
        var regex = /\/status\/(\d+)/;
        var match = url.match(regex);

        if (match && match[1]) {
            tweetID = match[1];
        }

        return tweetID;
    }
    // Function to plot a tweet
    async function plotTweet(tweetID) {
        console.log("Plotting tweet:", tweetID);
        var tweetContainer = document.getElementById('tweet-container');
        var tweetDiv = document.createElement('div');
        tweetDiv.setAttribute('id', 'tweet');
        tweetDiv.setAttribute('tweetID', tweetID);
        tweetContainer.appendChild(tweetDiv);

        await twttr.widgets.createTweet(tweetID, tweetDiv, {
            conversation: 'none', // or all
            cards: 'hidden', // or visible
            linkColor: '#cc0000', // default is blue
            theme: 'light', // or dark
        }).then(function (el) {
            el.contentDocument.querySelector('.footer').style.display = 'none';
        });


    }

    //Event Listeners
    document.getElementById('startBtn').addEventListener('click', async function () {
        // Show loading indicator
        document.getElementById('loading-indicator').style.display = 'block';

        try {
            // Save user likes for each player
            await Promise.all(players.map(async player => {
                console.log('waiting for likes')
                saveUserLikes(player);
                console.log('gotten likes')
            }));

            // Get mixed JSON data
            console.log('waiting for mixedJSON')
            const response = await getMixedJson();
            console.log('gottenJSON')

            console.log(response)

            // Plot tweets
            await Promise.all(response.tweets.map(async tweet => {
                console.log('waiting for plotting')
                const tweetID = getTweetIDFromURL(tweet);
                if (tweetID) {
                    plotTweet(tweetID);
                }
            }));
        } catch (error) {
            console.error('Error:', error);
        } finally {
            // Hide loading indicator after data is fetched
            document.getElementById('loading-indicator').style.display = 'none';
        }
    }); document.getElementById('addUser').addEventListener('click', addUser)
});



