from flask import Flask, render_template, request
import route_planner
import config

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html', gmaps_api_key = config.gmaps_api_key)

@app.route('/', methods = ['POST'])
def result():
    origin = request.form['origin']
    destinaton = request.form['destination']
    ordered_routes = route_planner.fastest_route(origin, destinaton,)
    return render_template('result.html', ordered_routes = ordered_routes, gmaps_api_key = config.gmaps_api_key)

if __name__ == '__main__':
    app.run(debug=False)