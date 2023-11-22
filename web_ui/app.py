from flask import Flask, render_template, jsonify, request, session
from ShortNLong import Game, Agent
import threading
import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return render_template("index.html")





@app.route("/game_state", methods = ["POST","GET"] )
def post_game_state():
    if request.method == "POST":
        data = dict(request.form)
        session["data"] = data
        return {'status': 'success', 'message': 'POST request successful', 'data': data}
    elif request.method == "GET":
        data = session.get("data", None)  # Use session.get to avoid KeyError

        if data is not None:
            return jsonify(data)
        return jsonify({'status': 'error', 'message': 'No data available for GET request'})

def run_app():
    app.run(debug=True,host="192.168.0.17",port=5000)



if __name__ == "__main__":
    tråd = threading.Thread(target=run_app())
    tråd.start()


