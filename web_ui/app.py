from flask import Flask, render_template, jsonify, url_for, request
from ShortNLong import Game, Agent
import threading
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")





@app.route("/post_game_state", methods = ["POST"] )
def post_game_state():
    if request.method == "POST":
        data = dict(request.form)
        return {'status': 'success', 'message': 'POST request successful', 'data': data}


def run_app():
    app.run(debug=True,host="192.168.0.17",port=5000)



if __name__ == "__main__":

    tråd = threading.Thread(target=run_app())
    tråd.start()
