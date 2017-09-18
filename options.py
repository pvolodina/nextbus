import requests
import json
import datetime


api_url_base = 'http://svc.metrotransit.org/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


# when a user asks for route options, this returns a list of all routes available
# a user must give the exact name (including route number) as given in the list,
# or if the route isn't a METRO route then the user can just input the route number

def show_routes():
	api_url = '{}NexTrip/Routes?format=json'.format(api_url_base)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	for i in range(len(data)):
		print('		' + data[i]['Description'])
	bus_route = input('Please provide the full bus route name: ')
	return bus_route


# when a user has selected their route of choice, this function returns the two
# possible directions of travel within that route

def show_directions(route):
	api_url = '{}NexTrip/Directions/{}?format=json'.format(api_url_base, route)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	direction = input('Are you traveling ' + data[0]['Text'] + ' or ' + data[1]['Text'] + ' today? ')
	return direction


# when a user asks for stop options, this returns a lost of all bus stops available
# for the previously selected bus route and direction
# a user must give the full bus stop name when selecting a bus stop, but if the
# 4-character stop identifier is known, that also works as input

def show_stops(bus_route, direction):
	api_url = '{}NexTrip/Stops/{}/{}?format=json'.format(api_url_base, bus_route, direction)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	if (len(data) == 0):
		print('There are no buses running on this route today :(')
		exit()
	for i in range(len(data)):
		print('		' + data[i]['Text'])
	bus_stop = input('Please provide the full bus stop name: ')
	return bus_stop


# when a user selects a route, the input is matched against a route in the API
# either by the exact route name or route number
# this function returns the route number of the desired route
# if the route isn't found, the program terminates
# TODO: allow a user to try inputting a route again if they failed on the first attempt without terminating the program

def get_route(bus_route):
	route = 0
	api_url = '{}NexTrip/Routes?format=json'.format(api_url_base)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	for i in range(len(data)):
		if (bus_route == data[i]['Description'] or bus_route == data[i]['Route']):
			route = data[i]['Route']
	if (route == 0):
		print('There were no routes found matching that name or route number :(')
		exit()
	return route


# when a user inputs a direction, this function checks to see if it was a valid
# input by checking the different possible ways they could have typed it
# this function returns the ID value of the direction by the API's documentation:
#		1 = South, 2 = East, 3 = West, 4 = North.
# there's probably a much easier way to check this instead of hard-coding them
# TODO: allow a user to try inputting a direction again without terminating the program

def get_direction(bus_route, d):
	direction = 0
	if (d == "SOUTH" or d == "SOUTHBOUND" or d == "southbound" or d == "South" or d == "south" or d == "S" or d == "s"):
		direction = 1
	elif (d == "EAST" or d == "EASTBOUND" or d == "eastbound" or d == "East" or d == "east" or d == "E" or d == "e"):
		direction = 2
	elif (d == "WEST" or d == "WESTBOUND" or d == "westbound" or d == "West" or d == "west" or d == "W" or d == "w"):
		direction = 3
	elif (d == "NORTH" or d == "NORTHBOUND" or d == "northbound" or d == "North" or d == "north" or d == "N" or d == "n"):
		direction = 4
	else:
		print('You have entered an invalid direction')
		exit()
	return direction


# when a user inputs their desired bus stop, this function takes the bus route
# and the direction and checks if the bus stop was valid
# the user can input either the bus stop name or the 4-character stop identifier
# TODO: allow a user to try again without terminating

def get_stop(bus_stop, bus_route, direction):
	stop = 0
	api_url = '{}NexTrip/Stops/{}/{}?format=json'.format(api_url_base, bus_route, direction)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	for i in range(len(data)):
		if (bus_stop == data[i]['Text'] or bus_stop == data[i]['Value']):
			stop = data[i]['Value']
	if (stop == 0):
		print('There were no buses found leaving this stop in this direction :(')
		exit()
	return stop


# this function parses the datetime value that the API returned, converts it
# to a datetime timestamp, then subtracts that timestamp from the time right
# now, and returns the floor(difference) of the minutes between the times

def parse_time(time):
	split1 = time.split("(")
	time = split1[1]
	split2 = time.split("-")
	time = split2[0]
	timestamp = int(time)
	bus_time = datetime.datetime.fromtimestamp(timestamp / 1000)
	now = datetime.datetime.now()
	diff = str(bus_time - now)
	split3 = diff.split(":")
	diff = split3[1]
	split4 = diff.split(":")
	diff = split4[0]
	if (diff[0] == "0"): 	# remove leading zero if minutes < 10
		return diff[1]
	else:
		return diff
