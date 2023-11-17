from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
app = Flask(__name__)
socket = SocketIO(app=app)
@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_game_state<agentID>')
def game_state():
    print("hej")
    return "hej"

@socket.on('message_from_frontend')
def handle_msg(data):
    print(data)
    socket.emit('message_from_backend', {'data': 'Hello from the backend!'})

def game_update():
    return "new element"

def hej():
    print(2)
if __name__ == "__main__":
    background_thread = threading.Thread(target=hej)
    background_thread.daemon = True
    background_thread.start()

    # Run the Flask app with multi-threading
    socket.run(app=app, debug=True)