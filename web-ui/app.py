from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_game_state')
def game_state():
    print("hej")
    return "hej"
if __name__ == "__main__":
    app.run(debug=True)