import requests
import json
import datetime


api_url_base = 'http://svc.metrotransit.org/'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

def show_routes():
	print('GETTING BUS ROUTE OPTIONS ...')
	api_url = '{}NexTrip/Routes?format=json'.format(api_url_base)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	for i in range(len(data)):
		print(data[i]['Description'])
	bus_route = input('Please provide the full bus route name: ')
	return bus_route

def show_stops(bus_route, direction):
	api_url = '{}NexTrip/Stops/{}/{}?format=json'.format(api_url_base, bus_route, direction)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	if (len(data) == 0):
		print('There are no buses running on this route today :(')
		exit()
	for i in range(len(data)):
		print(data[i]['Text'])
	bus_stop = input('Please provide the full bus stop name: ')
	return bus_stop

def show_directions(route):
	api_url = '{}NexTrip/Directions/{}?format=json'.format(api_url_base, route)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	direction = input('Are you traveling ' + data[0]['Text'] + ' or ' + data[1]['Text'] + ' today? ')
	return direction

def get_route(bus_route):
	route = 0
	api_url = '{}NexTrip/Routes?format=json'.format(api_url_base)
	resp = requests.get(url=api_url)
	data = json.loads(resp.text)
	for i in range(len(data)):
		if (bus_route == data[i]['Description'] or bus_route == data[i]['Route']):
			route = data[i]['Route']
	if (route == 0):
		print('Invalid route input, please choose from the following list:')
		route = show_routes()
	return route

def get_direction(bus_route, d):
	direction = 0
	if (d == "SOUTH" or d == "South" or d == "south" or d == "S" or d == "s"):
		direction = 1
	elif (d == "EAST" or d == "East" or d == "east" or d == "E" or d == "e"):
		direction = 2
	elif (d == "WEST" or d == "West" or d == "west" or d == "W" or d == "w"):
		direction = 3
	elif (d == "NORTH" or d == "North" or d == "north" or d == "N" or d == "n"):
		direction = 4
	else:
		print('You have entered an invalid direction')
		exit()
	return direction

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

def parse_time(time):
	split1 = time.split("(")
	time = split1[1]
	split2 = time.split("-")
	time = split2[0]
	timestamp_with_ms = int(time)
	bus_time = datetime.datetime.fromtimestamp(timestamp_with_ms / 1000)
	now = datetime.datetime.now()
	diff = str(bus_time - now)
	split3 = diff.split(":")
	diff = split3[1]
	split4 = diff.split(":")
	diff = split4[0]
	if (diff[0] == "0"):
		return diff[1]
	else:
		return diff
