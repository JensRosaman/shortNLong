from flask import Flask, jsonify, request
from ShortNLong import Game
import asyncio
import threading

# Handles several connections from diffrent endpoints and connects them to the main script
# recives instructions from main about players turn and reroutes it to the endpoint

class Server:
    def __init__(self, instID, newThread= True) -> None:
        self.instID = instID
        self.newThread = newThread
        self.app = Flask(__name__)
        with self.app.app_context():
            links = {}
        @self.app.route()
        def f():
    def run(self):
        if self.newThread:
            thread = threading.Thread(target=self.app.run)
        else:
            app.run()


def Main():
    app.run(host='192.168.1.66', port=5000)
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hej!'

    @app.route('/action/<action>')
    def get_player_turn(action):

if __name__ == "__main__":
    Main()