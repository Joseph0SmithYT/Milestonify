import flask
from flask import Flask, render_template, request, make_response
import os
import sys

# append a new directory to sys.path
sys.path.append('/home/cancri/dev-folder/Milestonify/main')
import main.milestonifyapp as milestonifyapp

app = Flask(__name__, template_folder='templates', static_folder='/static')

@app.route('/', methods=["POST", "GET"])
def contact():
    total_points = 0
    resp = make_response(render_template('index.html'))
    
    if not request.cookies.get('total_points') is None:
        total_points = int(request.cookies.get('total_points'))
    
    if request.method == "POST":
        task = request.form['task-input']
        if task == "":
            return render_template('index.html')

        points = milestonifyapp.submit_task(task, milestonifyapp.total_points)
        total_points += points  # Update total_points

        resp = make_response(render_template('index.html', total_points=total_points))
    
        if request.cookies.get('total_points') is None:
            resp.set_cookie('total_points', str(total_points))
    
        return resp  # Return the response with updated total_points
    else:
        return render_template('index.html', total_points=total_points)

@app.route('/test/')
def test():
    return 'Everything still working, trust.'

@app.route('/task/<task>')
def task(task):
    return f'{task}'

if __name__ == "__main__":
    app.run(debug=True)
