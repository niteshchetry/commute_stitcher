from googlemaps import Client
import json
import datetime
import config
from operator import methodcaller

#possible_bus_routes = [] #contains a list of BUS_ROUTE objects containing information about the primary bus route from origin to desitination
#creates client to make requests from google maps api, documentation: https://googlemaps.github.io/google-maps-services-python/docs/#module-googlemaps
gmaps = Client(key=config.gmaps_api_key)

# accepts an orgin and destination as array of coordinates
# searches for through the bus routes via google maps directions api
# creates a bus route object for the primary(farthest distance) leg of each route
# adds the bus route objects to a global list
def get_primary_bus_routes(origin, destination) :
  directions_results = gmaps.directions(origin, destination, mode = 'transit', arrival_time = datetime.datetime(2018, 12, 18, 10, 30), transit_routing_preference = 'fewer_transfers', alternatives = True)
  possible_bus_routes = set()
  for route in directions_results :
    direction_steps = route.get('legs')[0].get('steps') # json.dumps(json_object) removes of the 'u' before the python dict object version of the json
    farthest_step = 'error'
    farthest_step_value = 0
    for step in direction_steps :
      if (step.get('travel_mode') == 'TRANSIT') :
        direction_step_distance = step.get('distance').get('value')
        if(direction_step_distance > farthest_step_value) :
          farthest_step = step
          farthest_step_value = direction_step_distance
    possible_bus_routes.add(Bus_Route(farthest_step, origin, destination)) # ALSO DON'T add if they have the same departure stop & route number value
  return possible_bus_routes
'''
# accepts a location as an array of coordinates or string of address
# accepts radius to search for in miles
# returns closest park and rides
def get_nearby_bustops(location, radius):
    # checks if location is a string, if so, assumes it is an address
    # and uses helper function to convert to array of latitidue and longitude coordinates
    if (isinstance(location, basestring)) :
        location = return_coordinates(location)
    radius_in_meters = convert_miles_to_meters(radius)
    pNear_result = gmaps.places_nearby(location, radius_in_meters, name = 'part+and+ride') # type = 'transit station'
    return pNear_result.get('results')[0:1] # only returns the first place (list - can loop over later)


# accepts an address as a string
# returns an array of the latitude and longitude
def return_coordinates(address):
    geocode_result = gmaps.geocode(address) # auto converts from json to list of dictoinaries
    return [geocode_result[0].get('geometry').get('location').get('lat'), geocode_result[0].get('geometry').get('location').get('lng')]
'''
def convert_miles_to_meters(miles):
  return miles * 1609.344

# creates a new bus route with inputted transit_details
class Bus_Route :
  def __init__ (self, route, origin_address, destination_address):
    self.route_number = route.get('transit_details').get('line').get('short_name')
    self.route_name = route.get('transit_details').get('line').get('name')
    self.departure_stop_location = [route.get('transit_details').get('departure_stop').get('location').get('lat'), route.get('transit_details').get('departure_stop').get('location').get('lng')]
    self.departure_stop_name = route.get('transit_details').get('departure_stop').get('name')
    self.arrival_stop_location = [route.get('transit_details').get('arrival_stop').get('location').get('lat'), route.get('transit_details').get('arrival_stop').get('location').get('lng')]
    self.arrival_stop_name = route.get('transit_details').get('arrival_stop').get('name')
    self.departure_time = route.get('transit_details').get('departure_time').get('text')
    self.arrival_time = route.get('transit_details').get('arrival_time').get('text')
    self.transit_travel_time = route.get('duration').get('value')
    self.origin_address = origin_address
    self.destination_address = destination_address
    self.readable_driving_time = str((datetime.timedelta(seconds=self.get_driving_time())))
    self.readable_commute_time = str((datetime.timedelta(seconds=self.get_total_commute_time())))
    self.readable_walking_time = str((datetime.timedelta(seconds=self.get_walking_time())))
  
  def get_total_commute_time(self):
    return self.transit_travel_time + self.get_driving_time() + self.get_walking_time()

  def get_driving_time(self) :
    driving_directions = gmaps.directions(self.origin_address, self.departure_stop_location)
    driving_time = 0
    for step in driving_directions[0].get('legs') :
      driving_time += step.get('duration').get('value')
    return driving_time

  def get_walking_time(self) :
    walking_directions = gmaps.directions(self.arrival_stop_location, self.destination_address, mode = 'walking')
    walking_time = 0
    for step in walking_directions[0].get('legs') :
      walking_time += step.get('duration').get('value')
    return walking_time
  def __eq__(self, other):
    return self.route_number==other.route_number\
           and self.departure_stop_name==other.departure_stop_name\
           and self.departure_time==other.departure_time
  
  
  def __hash__(self):
    return hash((self.route_number, self.departure_stop_name, self.departure_time))
  
#returns a list of the routes from fasest to slowest total commute time (driving + transit)
def fastest_route(departure_address, arrival_address):
  possible_bus_routes = get_primary_bus_routes(departure_address, arrival_address)
  
  sorted_list = sorted(list(possible_bus_routes), key= lambda x: x.get_total_commute_time())
  # print(json.dumps(possible_bus_routes[0].driving_directions_to_departure_stop))
  return sorted_list
  '''('The fastest commuting method from ' + sorted_list[0].origin_address + ' to ' + sorted_list[0].destination_address + ' is to drive to ' + sorted_list[0].departure_stop_name
  + ' and then take bus route number ' + sorted_list[0].route_number + ' at ' + sorted_list[0].departure_time + ' to ' + sorted_list[0].arrival_stop_name
  + ' at ' + sorted_list[0].arrival_time + '\n The total commute time is ' + str((datetime.timedelta(seconds=sorted_list[0].get_total_commute_time()))))
'''
#fastest_route('12502 Hummingbird Ln, Mukilteo, WA 98275', '4069 Spokane Ln, Seattle, WA 98105')
# 12502 Hummingbird Ln, Mukilteo, WA 98275
# 4069 Spokane Ln, Seattle, WA 98105