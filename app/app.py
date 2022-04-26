from flask import Flask, render_template

app = Flask(__name__)

@app.route("/graphs")
def home():
    data = [
        ("01-01-2020", 1957),
        ("01-02-2020", 1958),
        ("01-03-2020", 1959),
        ("01-04-2020", 1960),

    ]

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("graph.html", labels = labels, values=values )