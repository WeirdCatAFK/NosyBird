document.addEventListener('DOMContentLoaded', function () {
    // Array to store the list of players
    let players = [];

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
    function clearTweetContainer() {
        var tweetContainer = document.getElementById("tweet-container");
        tweetContainer.innerHTML = ""; // Clearing inner HTML to remove all contents
    }

    // Function to send a POST request to restart likes
    async function restartLikes() {
        try {
            const response = await fetch('http://localhost:5000/restart_likes', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Something went wrong on the server');
            }

            const data = await response.text();
            console.log(data); // Log success message
        } catch (error) {
            console.error('Error:', error);
        }
    }


    // Function to fetch mixed JSON data from the server
    async function getMixedJson() {
        try {
            const response = await fetch('http://localhost:5000/get_mix');

            if (!response.ok) {
                throw new Error('Something went wrong on the server');
            }
            const data = await response.json();
            console.log(data); // Log retrieved JSON data
            return data;
        } catch (error) {
            console.error('Error:', error);
            throw error; // Re-throw the error to propagate it to the caller
        }
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
    function plotTweet(tweetID, user) {
        console.log("Plotting tweet:", tweetID);
        var tweetContainer = document.getElementById('tweet-container');

        // Create tweet div
        var tweetDiv = document.createElement('div');
        tweetDiv.setAttribute('class', 'tweet');
        tweetDiv.setAttribute('tweetID', tweetID);
        tweetContainer.appendChild(tweetDiv);

        // Create user div
        var userDiv = document.createElement('div');
        userDiv.setAttribute('class', 'user');
        userDiv.textContent = user;
        tweetContainer.appendChild(userDiv);

        // Load tweet
        twttr.widgets.createTweet(tweetID, tweetDiv, {
            conversation: 'none', // or all
            cards: 'hidden', // or visible
            linkColor: '#cc0000', // default is blue
            theme: 'light', // or dark
        });

        // Add click event to reveal user
        revealUserDiv.addEventListener('click', function () {
            revealUserDiv.style.display = 'none'; // Hide reveal box
            userDiv.classList.remove('hidden'); // Reveal user
        });
    }



    document.getElementById('startBtn').addEventListener('click', function () {
        // Show loading indicator start
        document.getElementById('loading-indicator').style.display = 'block';
        console.log(players);
        players.forEach(player => {
            saveUserLikes(player)
            console.log('saved')
        });
        //We replace the startBtn for a nextBtn
        document.getElementById('nextBtn').style.display = 'inline';

        document.getElementById("startBtn").style.display = 'None';
        //We wait 10 seconds or so to wait to get the likes of a person (I know there are better ways to implement this but this is what works best for me)
        setTimeout(async function () {
            data = await getMixedJson()
            console.log(data.user.splice(0, 1))
            //Plot an Inicial Tweet
            plotTweet(getTweetIDFromURL(data.tweets.splice(0, 1)[0]), data.user.splice(0, 1)[0])
            // Remove loading indicator finish
            document.getElementById('loading-indicator').style.display = 'None';

            setTimeout(async function () {
                restartLikes()
            }, 5000)

        }, 10000)


    });

    tweetCounter = 1
    document.getElementById('nextBtn').addEventListener('click', async function () {
        // Show loading indicator start
        document.getElementById('loading-indicator').style.display = 'block';
        clearTweetContainer();

        // Display another tweet
        console.log(data.user.splice(tweetCounter, 1));
        plotTweet(getTweetIDFromURL(data.tweets.splice(tweetCounter, 1)[0]), data.user.splice(tweetCounter, 1)[0]);

        tweetCounter++;

        // Remove loading indicator finish
        document.getElementById('loading-indicator').style.display = 'none';
    });

    document.getElementById('addUser').addEventListener('click', addUser);


});




