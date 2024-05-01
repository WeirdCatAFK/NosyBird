document.addEventListener('DOMContentLoaded', function () {
    // Array to store the list of players
    let players = [];

    function savePlayersLikes(username) {
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
                console.log(data); 
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    function clearTweetContainer() {
        var tweetContainer = document.getElementById("tweet-container");
        tweetContainer.innerHTML = ""; 
    }

    async function restartLikes() {
        try {
            const response = await fetch('http://localhost:5000/restart_likes', {
                method: 'POST'
            });

            if (!response.ok) {
                throw new Error('Something went wrong on the server');
            }

            const data = await response.text();
            console.log(data); 
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
            console.log(data); 
            return data;
        } catch (error) {
            console.error('Error:', error);
            throw error; 
        }
    }

    function addPlayer() {
        const userInput = document.getElementById('userInput').value.trim();

        if (userInput !== '') {
            players.push(userInput);

            // Create a new user element
            const newUser = document.createElement('div');
            newUser.className = 'user';
            newUser.textContent = userInput;
            const removeButton = document.createElement('button');
            removeButton.className = 'removePlayer';
            removeButton.textContent = 'Remove Player';
            removeButton.addEventListener('click', function () {
                const index = players.indexOf(userInput);
                if (index !== -1) {
                    players.splice(index, 1);
                }
                newUser.remove();
            });

            // Append the user element and remove button to the list
            newUser.appendChild(removeButton);
            document.getElementById('usersAlreadyPlaying').appendChild(newUser);

            document.getElementById('userInput').value = '';
        }
    }
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

        var tweetDiv = document.createElement('div');
        tweetDiv.setAttribute('class', 'tweet');
        tweetDiv.setAttribute('tweetID', tweetID);
        tweetContainer.appendChild(tweetDiv);

        var userDiv = document.createElement('div');
        userDiv.setAttribute('class', 'user');
        userDiv.textContent = user;
        tweetContainer.appendChild(userDiv);

        twttr.widgets.createTweet(tweetID, tweetDiv, {
            conversation: 'none', // or all
            cards: 'hidden', // or visible
            linkColor: '#cc0000', // default is blue
            theme: 'light', // or dark
        });
    }



    document.getElementById('startBtn').addEventListener('click', function () {
        // Show loading indicator start
        document.getElementById('loading-indicator').style.display = 'block';
        console.log(players);
        players.forEach(player => {
            savePlayersLikes(player)
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

    document.getElementById('addPlayer').addEventListener('click', addPlayer);


});




