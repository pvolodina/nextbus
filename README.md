# nextbus
A simple Python script that returns the amount of time until the next bus leaves a specified bus stop, using the API at http://svc.metrotransit.org/.

## how it works
The script contains only two files: nextbus.py and options.by, and it can be run simply by:
```
$ python nextbus.py
```
The script will wait for input from the user at every step of determining the exact bus that is leaving soonest from the desired bus stop.

The first input it will ask for is the name of the bus route on which the bus stop is located:
```
Which bus route do you want to use?
(Enter "options" or "o" to see options) 
```
Most of the bus routes have a route number associated with them, and if you select to bring up the options, that number is found to the left of the name of the route. You can input either the full name or just the route number. If you decide to enter the full route name, it must be entered exactly how it is named (including that route number) and is case-sensitive.

After selecting the bus route, you are asked for the desired direction that you want to travel along the route you chose. 
The program checks the possible directions allowed for that route, and then asks you which direction you want to choose:
```
Bus Route Selected:  METRO Blue Line
Are you traveling NORTHBOUND or SOUTHBOUND today? 
```
You can input the direction you want in multiple variations of north/south/east/west. For the above example, if you want to travel northbound, you can input it as any choice of {"NORTHBOUND", "NORTH", "Northbound", "North", "north", "N", "n"}.

After your desired direction is accepted, the program asks which bus stop along that route you are looking to depart from:
```
Direction Selected:  North
Which bus stop will you be leaving from?
(Enter "options" or "o" to see options) 
```
Again, you can view the possible options of bus stops along the route, and you must input the bus stop name exactly how it is named (case-sensitive). You can use the options to verify that the name you want is spelled correctly.

After your desired bus stop is accepted, the program then outputs the amount of minutes until the next bus departs from that stop:
```
Bus Stop Selected:  Target Field Station Platform 1
The next bus leaves in 11 minutes
```
