<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.1.2/socket.io.js"></script>



function startGame() {
    fetch('/start_game')
        .then(response => response.text())
        .then(data => {
            console.log(data); // Output success message in the console
            getGameState();
        })
        .catch(error => console.error('Error:', error));


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


class Player {
    constructor(id) {
        this.element = document.getElementById(id)
        this.id = id
        this.board = document.createElement('div');
        this.board.style.background = 'blue';    }
    
    
}
// location.hostname
const socket = io();

// Example: Send a message from frontend to backend
socket.emit('message_from_frontend', { data: 'Hello from the frontend!' });

// Example: Receive a message from backend
socket.on('message_from_backend', (data) => {
    console.log('Message from backend:', data);
});


document.getElementById('startGameBtn').addEventListener('click', startGame);
document.getElementById('makeMoveBtn').addEventListener('click', makeMove);
