import json

from flask import Flask, make_response, render_template, request

from wordle import Wordle

CLEAR_TOKEN = "batman"
app = Flask(__name__, static_folder="static")
w = Wordle("core/wordle_trim_out_pro.npy")


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
        print(w._blacklist)
        info, suggestions = w.suggest(word, pattern)
        return render_template(
            "render_suggestions.html", suggestions=suggestions, info=round(info, 4)
        )
    return (404,)


@app.route("/", methods=["GET"])
def main():
    w.reset()
    return render_template("index.html", suggestions=w._raw[:20], info=round(0.0, 4))
