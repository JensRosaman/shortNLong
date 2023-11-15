class Player {
    constructor(id, state) {
        this.id = id
        this.state = state;
        this.hand = state["hand"];
        this.board = document.createElement('div');
        this.board.style.background = 'blue';
        this.cards = document.createElement('p');
        cards.text = ''
    }
}

function startGame() {
    fetch('/start_game')
        .then(response => response.text())
        .then(data => {
            console.log(data); // Output success message in the console
            getGameState();
        })
        .catch(error => console.error('Error:', error));

    while (true) {
        // Your logic here
    }
}

function makeMove() {
    // Your logic to make a move goes here
    // You'll need to implement the move data and send it to the backend
    // For example, playing a card or declaring the hand
    fetch('/make_move', {
        method: 'GET', // Change the method as per your game's requirements
        headers: {
            'Content-Type': 'application/json'
            // Add any required headers
        },
        // Add your move data in the body if needed
    })
        .then(response => response.json())
        .then(data => {
            console.log(data); // Output game state or success message in the console
            getGameState();
        })
        .catch(error => console.error('Error:', error));
}

function getGameState() {
    fetch('/get_game_state')
        .then(response => response.json())
        .then(data => {
            document.getElementById('gameState').innerText = JSON.stringify(data, null, 2);
            // Update UI with game state data
        })
        .catch(error => console.error('Error:', error));
}

// Initial call to get the game state when the page loads
getGameState();

document.getElementById('startGameBtn').addEventListener('click', startGame);
document.getElementById('makeMoveBtn').addEventListener('click', makeMove);