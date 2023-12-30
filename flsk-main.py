import flask
from flask import Flask, render_template, request, make_response
import os
import sys
import json 


# append a new directory to sys.path
sys.path.append("C:/Users/amern/Downloads/Milestonify-main/Milestonify-main/")
import main.milestonifyapp as milestonifyapp

app = Flask(__name__, template_folder='templates', static_folder='/static')

@app.route('/', methods=["POST", "GET"])
def contact():
    task_list = []
    total_points = 0
    resp = make_response(render_template('index.html'))
    
    if 'total_points' in request.cookies:
        total_points = int(request.cookies['total_points'])
        print(total_points)
    if 'task_list' in request.cookies:
        task_list = json.loads(request.cookies['task_list'])
        print(task_list)
    
    if request.method == "POST":
        if 'reset' in request.form and request.form['reset'] == "Reset Data":
            task_list = []
            total_points = 0
            resp = make_response(render_template('index.html', total_points=total_points, task_list=task_list))
            resp.set_cookie('total_points', str(total_points))
            resp.set_cookie('task_list', json.dumps(task_list))
            return resp
    
        task = request.form['task-input']
        if task:
            points = milestonifyapp.submit_task(task, milestonifyapp.total_points)
            total_points += points
            task_list.append(task)
    
            resp = make_response(render_template('index.html', total_points=total_points, task_list=task_list))
    
            resp.set_cookie('total_points', str(total_points))
            resp.set_cookie('task_list', json.dumps(task_list))
            print('Added')
        print('Updated')
        return resp
    else:
        return render_template('index.html', total_points=total_points, task_list=task_list)


@app.route('/test/')
def test():
    return 'Everything still working, trust.'

@app.route('/task/<task>')
def task(task):
    return f'{task}'

if __name__ == "__main__":
    app.run(debug=True)
