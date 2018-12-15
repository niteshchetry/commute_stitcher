from flask import Flask
import route_calculator

app = Flask(__name__)

@app.route('/')
def hello_world():
    return route_calculator.fastest_route('***REMOVED***', '***REMOVED***')
