console.log("Script started")
let gameState;
var parent = document.getElementById('parent')
round = document.getElementById("round");


function startGame() {
    fetch('/start_game')
        .then(response => response.text())
        .then(data => {
            console.log(data); // Output success message in the console
            getGameState();
        })
        .catch(error => console.error('Error:', error));


}



function getGameState() {
    console.log("knapp tryckt")
    fetch('/game_state')
        .then(response => response.json())
        .then(data => {
            console.log(data)
            return data
        })
        .catch(error => console.error('Error:', error));
}


function updateUI() {
    // Updates the game ui with the info from the state
    let NewGameState = getGameState()
    if (gameState != null && JSON.stringify(NewGameState) === JSON.stringify(gameState)) {
        return;
    }
    gameState = NewGameState;

    let p = document.createElement("p")
    for (var child of parent.children){

        p.innerText = gameState["playerHands"][child.id].toString()
    }
}


class Player {
    constructor(id) {
        this.element = document.getElementById(id)
        this.id = id // id is number 1 - 5


    }
}

function game_loop(){
    // get intial game state
    let gameState = getGameState()




    var parent = document.getElementById('parent')
    let p = document.createElement("p")
    for (var child of parent.children){

        p.innerText = gameState["playerHands"][child.id]
    }

}



document.getElementById('startGameBtn').addEventListener('click', startGame());
document.getElementById('makeMoveBtn').addEventListener('click', makeMove);
