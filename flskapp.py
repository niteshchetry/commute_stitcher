from flask import Flask
import route_planner

app = Flask(__name__)

@app.route('/')
def hello_world():
    return route_planner.fastest_route('10801 Harbour Pointe Blvd, Mukilteo, WA 98275', '4069 Spokane Ln, Seattle, WA 98105')
