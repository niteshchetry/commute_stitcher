from flask import Flask, render_template, request
import route_planner
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html', gmaps_api_key = os.environ.get('gmaps_api_key', None))

@app.route('/', methods = ['POST'])
def result():
    origin = request.form['origin']
    destinaton = request.form['destination']
    date_time = str(request.form['date-time'])
    ordered_routes = route_planner.fastest_route(origin, destinaton, date_time)
    return render_template('result.html', ordered_routes = ordered_routes, gmaps_api_key = os.environ.get('gmaps_api_key', None))

if __name__ == '__main__':
    app.run(debug=False)