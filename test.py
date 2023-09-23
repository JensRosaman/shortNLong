from flask import Flask, jsonify, request , url_for
import asyncio
import threading

# Handles several connections from diffrent endpoints and connects them to the main script

def Main():
    app = Flask(__name__)

    @app.route("/t")
    def t():
        print("hej")

    with app.app_context():
        links = {"t": url_for("t")}
        print(links)
    


if __name__ == "__main__":
    p = {"d":{"pp":"gg"}}
    print(p)

