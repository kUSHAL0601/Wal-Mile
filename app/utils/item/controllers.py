from __future__ import division
from flask import *
from sqlalchemy.exc import IntegrityError
from app import *
from .models import Item

#from __future__ import print_function
# import print_function
# from __future__ import print_function
# import division
from urllib.request import urlopen
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import requests
import json
# import urllib

addr= ['3610+Hacks+Cross+Rd+Memphis+TN', # depot
                       '1921+Elvis+Presley+Blvd+Memphis+TN',
                       '149+Union+Avenue+Memphis+TN',
                       '1034+Audubon+Drive+Memphis+TN',
                       '1532+Madison+Ave+Memphis+TN',
                       '706+Union+Ave+Memphis+TN',
                       '3641+Central+Ave+Memphis+TN',
                       '926+E+McLemore+Ave+Memphis+TN',
                       '4339+Park+Ave+Memphis+TN',
                      ]

def create_data(addresses):
  """Creates the data."""
  data = {}
  data['API_key'] = 'AIzaSyBbS0obmG1Mn1oS-94qsLzi5tb0xx2DhgI'
  data['addresses'] = addresses
  return data

def create_distance_matrix(data):
  addresses = data["addresses"]
  API_key = data["API_key"]
  # Distance Matrix API only accepts 100 elements per request, so get rows in multiple requests.
  max_elements = 100
  num_addresses = len(addresses) # 16 in this example.
  # Maximum number of rows that can be computed per request (6 in this example).
  max_rows = max_elements // num_addresses
  # num_addresses = q * max_rows + r (q = 2 and r = 4 in this example).
  q, r = divmod(num_addresses, max_rows)
  dest_addresses = addresses
  distance_matrix = []
  # Send q requests, returning max_rows rows per request.
  for i in range(q):
    origin_addresses = addresses[i * max_rows: (i + 1) * max_rows]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)

  # Get the remaining remaining r rows, if necessary.
  if r > 0:
    origin_addresses = addresses[q * max_rows: q * max_rows + r]
    response = send_request(origin_addresses, dest_addresses, API_key)
    distance_matrix += build_distance_matrix(response)
  return distance_matrix

def send_request(origin_addresses, dest_addresses, API_key):
  """ Build and send request for the given origin and destination addresses."""
  def build_address_str(addresses):
    # Build a pipe-separated string of addresses
    address_str = ''
    for i in range(len(addresses) - 1):
      address_str += addresses[i] + '|'
    address_str += addresses[-1]
    return address_str

  request = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
  origin_address_str = build_address_str(origin_addresses)
  dest_address_str = build_address_str(dest_addresses)
  request = request + '&origins=' + origin_address_str + '&destinations=' + \
                       dest_address_str + '&key=' + API_key
  jsonResult = urlopen(request).read()
  response = json.loads(jsonResult)
  return response

def build_distance_matrix(response):
  distance_matrix = []
  for row in response['rows']:
    # row_list = [row['elements'][j]['distance']['value'] for j in range(len(row['elements']))]
    row_list = [row['elements'][j]['duration']['value'] for j in range(len(row['elements']))]
    distance_matrix.append(row_list)
  return distance_matrix

def create_data_model(time_matrix,dmnd,cp):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = time_matrix
    data['demands'] = [0]+dmnd
    data['vehicle_capacities'] = cp
    data['num_vehicles'] = len(cp)
    data['depot'] = 0
    return data

def print_solution(data, manager, routing, assignment, addr_list):
    """Prints assignment on console."""
    total_distance = 0
    total_load = 0
    vehicle_dict={}
    for vehicle_id in range(data['num_vehicles']):
        vehicle_dict[vehicle_id]=[]
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            vehicle_dict[vehicle_id].append(addr_list[node_index])
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(
            manager.IndexToNode(index), route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    return vehicle_dict


def main(addr,dmnd,cp):
    data=create_data(addr)
    time_matrix=create_distance_matrix(data)
    # print(time_matrix)
    data = create_data_model(time_matrix,dmnd,cp)
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if assignment:
        return print_solution(data, manager, routing, assignment,addr)
    return {}



mod_item = Blueprint('item', __name__)

@mod_item.route('/item', methods=['GET'])
def render_item_page():
	print("Here")
	return render_template('item.html')

@mod_item.route('/item/add', methods=['POST'])
def create_item():
    try:
        # item_id = request.form['item_id']
        height = request.form['height']
        width = request.form['width']
        fragile = request.form['fragile']
        status = request.form['status']
        client_id = request.form['client_id']
        vehicle_no = request.form['vehicle_no']
        weight = request.form['weight']
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400

    i = Item(height, weight, fragile, status, client_id, vehicle_no, weight, "NA")
    db.session.add(i)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This item already exists"), 400

    return jsonify(success=True)

@mod_item.route('/item/get', methods=['GET'])
def get_item():
	all_items= Item.query.filter(Item.client_id=="NA").all()
	ans=[]
	for i in all_items:
		ans.append([i.item_id,i.height,i.width,i.weight,i.fragile])
	return jsonify(ans)

@mod_item.route('/item/remove', methods=['POST'])
def remove_item():
    try:
        item_id = int(request.form['itd'])
        print(item_id)
    except KeyError as e:
        return jsonify(success=False, message="%s not sent in the request" % e.args), 400
    u=Item.query.filter(Item.item_id==item_id).first()
    db.session.delete(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return jsonify(success=False, message="This item already exists"), 400

    return jsonify(success=True)


# @mod_item.route('/item/vrp', methods=['GET'])
# def vrp():
# 	locv=addr
# 	item_vol= [1, 2, 4, 2, 4, 8, 8, 1]
# 	vehicle_cap=[15, 15, 15, 15]
# 	print(main(locv,item_vol,vehicle_cap))
# 	return "True"
	# return jsonify()

@mod_item.route('/VRP', methods=['GET'])
def get_data():
	import json
	client_ids = Item.query.filter(Item.status=="NOT_DELIVERED").all()
	loc=[]
	item_vol=[]
	for i in client_ids:
		loc.append(i.location)
		item_vol.append(int(i.width)*int(i.height))
	import urllib3
	http = urllib3.PoolManager()
	r=http.request("GET","localhost:8080/vehicle/getAll")
	print(json.loads(r.data))
	vehicle_nos=[]
	vehicle_cap=[]
	for i in json.loads(r.data):
		vehicle_nos.append(i[0])
		vehicle_cap.append(i[1])
	loc=addr
	item_vol= [1, 2, 4, 2, 4, 8, 8, 1]
	vehicle_cap=[15, 15, 15, 15]
	return jsonify({"0":[],"1":["12.92601741,77.6740694", "12.95303674,77.6984024", "12.98013678,77.67539978", "12.98047133,77.63935089", "12.94099133,77.62784958"],"3":["11.92601741,30.6740694", "18.95303674,80.6984024", "9.98013678,100.67539978", "32.98047133,97.63935089", "16.94099133,57.62784958"],"4":[]})
	# return jsonify(main(loc,item_vol,vehicle_cap))