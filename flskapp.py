from flask import Flask
import route_planner

app = Flask(__name__)

@app.route('/')
def hello_world():
    return route_planner.fastest_route('***REMOVED***', '***REMOVED***')
