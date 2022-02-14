import json

from flask import Flask, make_response, render_template, request

from wordle import Wordle

CLEAR_TOKEN = "batman"
app = Flask(__name__, static_folder="static")
w = Wordle()


@app.route("/reset", methods=["POST"])
def reset():
    return 404


@app.route("/process", methods=["POST"])
def process():
    data = request.data
    if data:
        data = json.loads(data)
        pattern = data.get("pattern").lower()
        word = data.get("word").lower()
        possible = data.get("possible").lower()
        w.update(word, possible)
        print(w._blacklist)
        return render_template(
            "render_suggestions.html", suggestions=w.suggest(pattern, possible)
        )
    return (404,)


@app.route("/", methods=["GET"])
def main():
    w.reset()
    return render_template("index.html", suggestions=w.suggest())
