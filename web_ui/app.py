from flask import Flask, render_template, jsonify, request, session, url_for
from flask_socketio import SocketIO
import threading
import secrets
import subprocess
import socket
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)
app.static_folder = 'static'
#app.config['SERVER_NAME'] = 'localhost:5000'
def get_ipv4_address():
    try:
        result = subprocess.run(["ipconfig"], capture_output=True, text=True)
        output = result.stdout

        # Parse the output to extract the IPv4 address
        for line in output.split("\n"):
            if "IPv4 Address" in line:  # Adjust this condition as needed
                ipv4_address = line.split(":")[-1].strip()
                return ipv4_address

        # If IPv4 address not found in output
        return None
    except Exception as e:
        print("Error occurred while getting local IPv4 address:", e)
        return None


app.config['SERVER_NAME'] =  get_ipv4_address() + ':5000'

stateData = None

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/hiddenUI/<agentID>")
def hidden_ui(agentID):
    return render_template("hiddenUI.html", agentID=agentID)
@app.route("/game_state", methods = ["POST","GET"] )
def post_game_state():
    global stateData
    if request.method == "POST":
        data = request.json
        print(f"Sending the game state to the frontend:")

        session["data"] = data
        stateData = data
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

            global agentResponse
            agentResponse = None
            # data is {"agentID":, "request":}

            socketio.emit("uiAgentRequest", request.json, callback=ui_agent_response)

            # Start a new thread to run wait_for_response in the background
            responseThread = threading.Thread(target=wait_for_response)
            responseThread.start()
            # Wait for the background thread to finish
            responseThread.join()
            print("returning response", agentResponse)
            return agentResponse
        return ""

def wait_for_response():
    global agentResponse
    while agentResponse is None:
        1 +3


@socketio.on(message="uiAgentResponse")
def ui_agent_response(ans):
    global agentResponse
    agentResponse = ans


@socketio.on("test")
def onConnection(data):
    socketio.emit("game_state", stateData)
    print(data)
    print(f"url for hidden is {get_ipv4_address() + url_for('hidden_ui', agentID=1)}")


def run_app():
    # , host="localhost"
    socketio.run(app=app, debug=True, host="0.0.0.0", allow_unsafe_werkzeug=True)



# 192.168.0.17

if __name__ == "__main__":
    thread = threading.Thread(target=run_app())
    thread.start()


