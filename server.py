from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')
