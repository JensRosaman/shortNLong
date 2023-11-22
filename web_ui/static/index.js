console.log("hek")



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
        })
        .catch(error => console.error('Error:', error));
}




class Player {
    constructor(id) {
        this.element = document.getElementById(id)
        this.id = id // id is number 1 - 5


    }
}

function game_loop(){
    // get intial game state
    let gameState ;
    fetch('/get_game_state')
        .then(response => response.json())
        .then(data => {
            gameState = data;
        })
        .catch(error => console.error('Error:', error));

    var parent = document.getElementById('parent')
    let p = document.createElement("p")
    for (var child of parent.children){

        p.innerText = gameState["playerHands"][child.id]
    }

}


document.getElementById('startGameBtn').addEventListener('click', startGame());
document.getElementById('makeMoveBtn').addEventListener('click', makeMove);
