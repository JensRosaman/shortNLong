from flask import Flask, render_template, jsonify, url_for, request
from ShortNLong import Game, Player, Agent
import threading
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_game_state')
def get_game_state():
    state = game.get_gamestate()
    return jsonify(state)



@app.route("/post_game_state", methods = ["POST"] )
def post_game_state():
    if request.method == "POST":
        data = request.form

def run_app():
    app.run(debug=True)



if __name__ == "__main__":
    spelare = [1, 2, 3, 4, 5]
    for i in spelare:
        spelare[spelare.index(i)] = Agent(i)
    game = Game(spelare, guiActive=True)
    game.start_game()

    tråd = threading.Thread(target=run_app())
    tråd.start()
