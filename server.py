from flask import Flask, render_template, request, redirect, url_for, jsonify
from calcuMLator import estimate

app = Flask(__name__, static_folder="docs")
op_strings = estimate.conf['types']
method_strings = estimate.conf['estimators']


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


@app.route('/compute')
def compute():
    n1 = request.args.get('n1')
    n2 = request.args.get('n2')
    op = request.args.get('op')
    method = request.args.get('method')
    if not all([n1, n2, op]) or op not in op_strings or method not in\
            method_strings or not is_number(n1) or not is_number(n2):
        return jsonify({'result': 'wrong query'})
    else:
        result = estimate.predict(float(n1), float(n2), op, method)
        return jsonify({'result': result})


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
