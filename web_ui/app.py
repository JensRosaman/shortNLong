from flask import Flask, render_template, jsonify, request, session
from flask_socketio import SocketIO
from ShortNLong import Game, Agent
import threading
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)
app.static_folder = 'static'


@app.route('/')
def index():
    return render_template("index.html")
@app.route("/game_state", methods = ["POST","GET"] )
def post_game_state():
    if request.method == "POST":
        data = dict(request.form)
        session["data"] = data
        socketio.emit("game_state", data)
        return {'status': 'success', 'message': 'POST request successful', 'data': data}
    elif request.method == "GET":
        data = session.get("data", None)

        if data is not None:
            return jsonify(data)
        return jsonify({'status': 'error', 'message': 'No data available for GET request'})



@app.route("/request_agent", methods = ["POST", "GET"])
def request_agent():
        if request.method == "POST":
            # data is {"agentID":, "request":}
            data = dict(request.form)
            socketio.emit("uiAgentRequest", data)
            return {'status': 'success', 'message': 'POST request successful', 'data': data}
        return ""
@socketio.on("test")
def test(data):
    print(data)
    return ""

def run_app():
    socketio.run(app=app, debug=True,host="192.168.0.17",port=5000, allow_unsafe_werkzeug=True)

# 192.168.0.17

if __name__ == "__main__":
    thread = threading.Thread(target=run_app())
    thread.start()


