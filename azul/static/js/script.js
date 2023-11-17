// script.js
document.addEventListener('DOMContentLoaded', function() {
    updateGameState(); // Initial call to populate the game board


    // Declare global variables to store user selections
    var selectedFactoryId = null;
    var selectedTileColor = null;
    var selectedDestination = null;
    var currentPlayerId = null;

    function createTile(color, isPlaceholder=false, context, contextId, isFirst=false) {
//        if (isFirst) {
//            var tile = document.getElementById('first-player-marker')
//        } else {
            var tile = document.createElement('div');
            tile.className = 'tile' + (isPlaceholder ? ' empty' : ' ' + color);
            if (context === 'factory') {
                tile.addEventListener('click', function() {
                    onFactoryTileClick(contextId, color);
                });
            } else if (context === 'patternLine') {
                tile.addEventListener('click', function() {
                    onPatternLineClick(contextId);
                });
            } else if (context === 'floorLine') {
                tile.addEventListener('click', function() {
                    onFloorLineClick();
                });
            }
//        }

        return tile;
    }

    function populateFactory(factoryId, tileColors) {
        var factory = document.getElementById('factories-section');
        var factoryDiv = document.createElement('div');
        factoryDiv.className = 'factory';
        var factoryLabel = document.createElement('span');
        factoryLabel.textContent = factoryId;
        factoryDiv.appendChild(factoryLabel);

        tileColors.forEach(function(color) {
            factoryDiv.appendChild(createTile(color, false, "factory", factoryId, false));
        });
        factory.appendChild(factoryDiv);
    }

    function populatePatternLines(playerId, patternLines) {
        var patternLinesDiv = document.getElementById('player' + playerId + ':pattern-lines-section');
        patternLinesDiv.innerHTML = ''; // Clear existing pattern lines

        var patternLinesLabelId = 'player-patternLine-' + playerId;
        var patternLinesLabel = document.getElementById(patternLinesLabelId);
        if (!patternLinesLabel) {
            patternLinesLabel = document.createElement('span');
            patternLinesLabel.id = patternLinesLabelId;
            patternLinesDiv.insertBefore(patternLinesLabel, patternLinesDiv.firstChild); // Insert at the beginning
        }

        patternLinesLabel.textContent = 'Pattern Line';
        patternLinesDiv.appendChild(patternLinesLabel);

        patternLines.forEach(function(line, index) {
            var lineDiv = document.createElement('div');
            lineDiv.className = 'pattern-line';
            lineDiv.id = 'player' + playerId + ':pattern-line' + index

            // The number of spaces in each line equals its index + 1
            var numberOfSpaces = index + 1;

            for (var i = 0; i < numberOfSpaces; i++) {
                // Check if there is a tile in this space, else create an empty tile
                var tileColor = line[i];
                var tile = createTile(tileColor ? tileColor : '', tileColor ? false : true, "patternLine", index, false); // Empty tile if tileColor is falsy
                lineDiv.appendChild(tile);
            }

            patternLinesDiv.appendChild(lineDiv);
        });
    }

    function populateWall(playerId, wallData) {
        var wallSection = document.getElementById("player" + playerId + ":wall-section");
        wallSection.innerHTML = ''; // Clear the existing wall

        var wallLabelId = 'player-wall-' + playerId;
        var wallLabel = document.getElementById(wallLabelId);
        if (!wallLabel) {
            wallLabel = document.createElement('div');
            wallLabel = document.createElement('span');
            wallLabel.id = wallLabelId;
            wallSection.insertBefore(wallLabel, wallSection.firstChild); // Insert at the beginning
        }

        wallLabel.textContent = 'Wall';
        wallSection.appendChild(wallLabel);

        for (var row = 0; row < 5; row++) {
            var rowDiv = document.createElement('div');
            rowDiv.className = 'wall-row';

            for (var col = 0; col < 5; col++) {
                // Check if there is a tile in this space, else create an empty tile
                var tileColor = (wallData[row] && wallData[row][col]) ? wallData[row][col] : '';
                var tile = createTile(tileColor, tileColor === '', "wall", 0, false);

                rowDiv.appendChild(tile);
            }

            wallSection.appendChild(rowDiv);
        }
    }

    function populateFloorLine(playerId, floorLineData) {
        var floorLineSection = document.getElementById('player' + playerId + ':floor-line-section');
        floorLineSection.innerHTML = ''; // Clear existing floor line

        var floorLineLabelId = 'player-floorLine-' + playerId;
        var floorLineLabel = document.getElementById(floorLineLabelId);
        if (!floorLineLabel) {
            floorLineLabel = document.createElement('div');
            floorLineLabel.className = 'floor-line-label';
            floorLineLabel.id = floorLineLabelId;
            floorLineSection.insertBefore(floorLineLabel, floorLineSection.firstChild); // Insert at the beginning
        }

        floorLineLabel.textContent = 'Floor Line';
        floorLineSection.appendChild(floorLineLabel);

        // Array of deduction points for each tile space in the floor line
        var deductionPoints = [-1, -1, -2, -2, -2, -3, -3];

        var lineDiv = document.createElement('div');
        lineDiv.className = 'floor-line';
        // Create 7 spaces for the floor line
        for (var i = 0; i < 7; i++) {

            var tileColor = floorLineData[i] ? floorLineData[i] : '';
            var isFirst = floorLineData[i] === 'F';
            var tile = createTile(tileColor ? tileColor : '', !tileColor, "floorLine", 0, isFirst); // Empty tile if tileColor is falsy

            // Create a span for the deduction points and add it to the tile
            console.log("floor data: ", floorLineData[i])
            console.log("deductionSpan: ", deductionSpan)
            var deductionSpan = document.createElement('span');
            deductionSpan.className = 'deduction-points';
            deductionSpan.textContent = deductionPoints[i];
            tile.appendChild(deductionSpan);

            lineDiv.appendChild(tile);
        }
        floorLineSection.append(lineDiv);
    }


    // Populate factories with placeholder content
//    populateFactory(0, ['blue', 'red', 'yellow', 'black', 'white']);

    // Populate pattern lines with placeholders
//    populatePatternLines([
//        ['blue', '', '', '', ''], // Example pattern line with one blue tile
//        ['red', 'red', '', '', ''], // Two red tiles
//        // ... more lines
//    ]);

    // Populate the wall with placeholders
//    populateWall([
//        ['blue', '', 'yellow', '', 'red'],
//        ['black', '', 'white', '', ''],
//        // ... more rows
//    ]);
//
//    // Populate the floor line with placeholders

    function updateGameState() {
        fetch('/get_game_state')
        .then(response => response.json())
        .then(function(gameState) {
            if (gameState.isGameOver) {
                alert("Game Over");
                // Stop the interval if set
                clearInterval(updateInterval);
            } else {
                // Update the game board here using gameState data
                // Assuming 'gameState' is an object with properties like 'factories', 'patternLines', etc.
                console.log('Received game state:', gameState);
                currentPlayerId = gameState.currentPlayerId
                var factoriesSection = document.getElementById('factories-section');
                factoriesSection.innerHTML = ''; // Clear existing factories

                gameState.factories.forEach(function(factory){
                    var factoryKey = Object.keys(factory)[0]; // Gets the first (and only) key in the object
                    var tiles = factory[factoryKey]; // Access the value using the key
                    populateFactory(factoryKey, tiles);
                });

                var centerKey = Object.keys(gameState.center)[0]
                var tiles = gameState.center[centerKey]; // Access the value using the key
                populateFactory(centerKey, tiles);

                gameState.players.forEach(function(playerData, index) {
                    populatePlayerArea(index, playerData, gameState.isRoundOver);
                });

            }
        }).catch(function(error) {
            console.error('Error fetching game state:', error);
        });
    }

    // Assuming you set an interval like this
//    var updateInterval = setInterval(updateGameState, 5000);



    function populatePlayerArea(playerId, playerData, isRoundOver) {
        var playerSection = document.getElementById('player' + playerId + '-section');
//        playerSection.innerHTML = '';
        var playerLabelId = 'player-label-' + playerId;
        var playerLabel = document.getElementById(playerLabelId);
        if (!playerLabel) {
            playerLabel = document.createElement('span');
            playerLabel.id = playerLabelId;
            playerSection.insertBefore(playerLabel, playerSection.firstChild); // Insert at the beginning
        }

        playerLabel.textContent = 'Player ' + playerId + ' - Score: ' + playerData.score;
        playerSection.appendChild(playerLabel);
        if (isRoundOver) {

        } else {
            populatePatternLines(playerId, playerData.patternLines)
            populateWall(playerId, playerData.wall)
            populateFloorLine(playerId, playerData.floor)

        }
//        playerSection.innerHTML = ''; // Clear existing content

        // Populate pattern lines, wall, and floor line for the player
        // Use playerData to get the state for this player's pattern lines, wall, and floor line
    }

    function onFactoryTileClick(factoryId, tileColor) {
        clearHighlights();
        // Highlight all tiles with the same color in the selected factory
        document.querySelectorAll('#factory-' + factoryId + ' .tile.' + tileColor).forEach(function(tile) {
            tile.classList.add('highlight');
        });
        selectedFactoryId = factoryId;
        selectedTileColor = tileColor;
        // Logic to highlight selected factory tile or provide visual feedback
        console.log('Selected Factory:', factoryId, 'Tile Color:', tileColor);
        // Check if a destination has been selected, then send the action
        sendActionIfComplete();
    }

    function onPatternLineClick(patternLineId) {
        clearHighlights();

        // Highlight the clicked pattern line
        clickedPatternlineId = 'player' + currentPlayerId + ':pattern-line' + patternLineId
        document.getElementById(clickedPatternlineId).classList.add('highlight');
        selectedDestination = 'patternLine-' + patternLineId;
        // Logic to highlight selected pattern line
        console.log('Selected Pattern Line:', patternLineId);
        // Check if a factory and tile color have been selected, then send the action
        sendActionIfComplete();
    }

    function onFloorLineClick() {
        clearHighlights();
        // Highlight the floor line

        document.getElementById('player-floorLine-' + currentPlayerId).classList.add('highlight');
        selectedDestination = 'floorLine';
        // Logic to highlight the floor line
        // Check if a factory and tile color have been selected, then send the action
        sendActionIfComplete();
    }

    function sendActionIfComplete() {
        if (selectedFactoryId !== null && selectedTileColor !== null && selectedDestination !== null) {
            var action = {
                factoryId: selectedFactoryId,
                tileColor: selectedTileColor,
                destination: selectedDestination,
                currentPlayerId: currentPlayerId
            };
            sendActionToServer(action); // Function to send action to server

            // Reset the selections
            selectedFactoryId = null;
            selectedTileColor = null;
            selectedDestination = null;
        }
    }

    function sendActionToServer(action) {
        fetch('/send_action', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(action)
        })
        .then(response => response.json())
        .then(updatedGameState => {
            // Update the game state with the response
            updateGameState();
        })
        .catch(error => console.error('Error sending action:', error));
    }

    function clearHighlights() {
        // Remove existing highlights
        document.querySelectorAll('.highlight').forEach(function(element) {
            element.classList.remove('highlight');
        });
    }

    function updateNotification(message) {
        var banner = document.getElementById('notification-banner');
        banner.textContent = message;
    }
});
