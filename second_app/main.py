from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__)

URL = "https://ttq8wo.deta.dev/"


@app.route('/', methods=["GET","POST"])
def hello_world():


    return render_template("index.html")