from flask import Flask, redirect, url_for, render_template, request, flash
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

URL = "https://ttq8wo.deta.dev/"


@app.route('/', methods=["GET", "POST"])
def hello_world():
    return render_template("index.html")


@app.route('/logger', methods=["GET", "POST"])
def logger():
    app.logger.debug('This is a debug message')
    print("this a debug message in python")
    return render_template("logger.html")


if __name__ == '__main__':
    app.run(debug=True)
