import options
import requests
import json


api_url_base = 'http://svc.metrotransit.org/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


# user enters the name or stop number of the route they want to use

bus_route = input('Which bus route do you want to use?\n(Enter "options" to see options) ')
if (bus_route == "options" or bus_route == "o"):
	bus_route = options.show_routes()
print('Bus Route Selected: ', bus_route)	# prints out what the user inputted
bus_route = options.get_route(bus_route)
#print('Bus Route ID: ', bus_route)			# used for debugging


# after the route is selected, the GetDirections() operation finds
# the two possible directions for that route, instead of the user
# manually choose between four directions (more user friendly approach)

direction = options.show_directions(bus_route)
print('Direction Selected: ', direction)
direction = options.get_direction(bus_route, direction)
#print('Direction ID: ', direction)


# after choosing the route and direction, the GetStops() operation
# finds all the possible bus stops for that route in that direction,
# this would prevent a user choosing a bus stop that doesn't exist
# on their previously selected route

bus_stop = input('Which bus stop will you be leaving from?\n(Enter "options" to see options) ')
if (bus_stop == "options" or bus_stop == "o"):
	bus_stop = options.show_stops(bus_route, direction)
print('Bus Stop Selected: ', bus_stop)
bus_stop = options.get_stop(bus_stop, bus_route, direction)
#print('Bus Stop ID: ', bus_stop)


# now that the route, direction, and stop are determined, the
# GetTimepointDepartures() operation provides the times of the remaining
# departure times for that bus stop for the day
# the first time returned is the soonest departing bus, so that time is
# parsed and the time difference between now and then is returned

#url = '{}NexTrip/{}/{}/{}?format=json'.format(api_url_base, "901", "1", "TF12") # debugging
url = '{}NexTrip/{}/{}/{}?format=json'.format(api_url_base, bus_route, direction, bus_stop)
resp = requests.get(url=url)
data = json.loads(resp.text)
dept_time = data[0]['DepartureTime']
minutes = options.parse_time(dept_time)

if (int(minutes) == 1):
	print('The next bus leaves in ' + minutes + ' minute')
elif (int(minutes) > 1):
	print('The next bus leaves in ' + minutes + ' minutes')
else:
	print('There are no buses leaving from this stop :(')
