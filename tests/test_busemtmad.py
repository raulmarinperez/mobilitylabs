#!/usr/bin/python3
from mobilitylabs.busemtmad import BusEMTMad
from datetime import datetime
import configparser
import argparse
import logging
import pprint
import sys
import os

# Auxiliary functions
#
def info_lines(busemtmad_service):
  today_string = datetime.today().strftime('%Y%m%d')
  info_lines = busemtmad_service.info_lines(today_string)

  if info_lines!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_lines)
  else:
    print("The BusEMTMad service didn't return any data.")

def info_line(busemtmad_service, line_id):
  today_string = datetime.today().strftime('%Y%m%d')
  info_line = busemtmad_service.info_line(line_id, today_string)

  if info_line!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_line)
  else:
    print("The BusEMTMad  service didn't return any data.")

def info_stops(busemtmad_service):
  info_stops = busemtmad_service.info_stops()

  if info_stops!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_stops)
  else:
    print("The BusEMTMad service didn't return any data.")

def info_stop(busemtmad_service, stop_id):
  info_stop = busemtmad_service.info_stop(stop_id)

  if info_stop!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_stop)
  else:
    print("The BusEMTMad  service didn't return any data.")

def line_stops(busemtmad_service, line_id, direction):
  line_stops = busemtmad_service.line_stops(line_id, direction)

  if line_stops!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(line_stops)
  else:
    print("The BusEMTMad  service didn't return any data.")

def issues(busemtmad_service, stop_id):
  issues = busemtmad_service.issues(stop_id)

  if issues!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(issues)
  else:
    print("The BusEMTMad  service didn't return any data.")

def buses_arrivals(busemtmad_service, stop_id, line_id):
  if line_id!=None:
    buses_arrivals = busemtmad_service.buses_arrivals(stop_id, line_id)
  else:
    buses_arrivals = busemtmad_service.buses_arrivals(stop_id)

  if buses_arrivals!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(buses_arrivals)
  else:
    print("The BusEMTMad  service didn't return any data.")

# Setting up debuging level and debug file with environment variables
#
debug_level = os.environ.get('MOBILITYLABS_DEBUGLEVEL',logging.WARN)
debug_file = os.environ.get('MOBILITYLABS_DEBUGFILE')

if debug_file==None:
  logging.basicConfig(level=debug_level)
else:
  logging.basicConfig(filename=debug_file, filemode='w', level=debug_level)

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['info_lines', 'info_line', 'info_stops', 'info_stop', 'line_stops', 
                                       'issues', 'buses_arrivals'],
                    help="what is going to be requested to the BusEMTMad service")
parser.add_argument("credentials_file", help="path to the file with info to access the service")
parser.add_argument("-lid", "--line_id",
                    help="bus line identifier for actions 'info_line', 'line_stops' and 'issues'; this argument is optional for action 'buses_arrivals'")
parser.add_argument("-sid", "--stop_id",
                    help="stop identifier for action 'info_stop' and 'buses_arrivals'")
parser.add_argument("-dir", "--direction", choices=['1','2'],
                    help="direction to be considered to analyze line info for action 'line_stops'; 1 for start to end, 2 for end to start")
args = parser.parse_args()

# Read credentials to instantiate the class to use the service
#
credentials = configparser.ConfigParser()
credentials.read(args.credentials_file)

x_client_id = credentials['DEFAULT']['x_client_id']
pass_key = credentials['DEFAULT']['pass_key']
busemtmad_service = BusEMTMad(x_client_id, pass_key)
busemtmad_service.log_in()

# Action dispatching if credentials logged the client into the service
#
if (busemtmad_service.is_logged_in()):
  if args.action == "info_lines":
    logging.debug("x_client_id '%s' asking for lines information" % x_client_id)
    info_lines(busemtmad_service)
  elif args.action == "info_line":
    if args.line_id!=None:
      logging.debug("x_client_id '%s' asking for information for bus line '%s'" %
                    (x_client_id, args.line_id))
      info_line(busemtmad_service, args.line_id)
    else:
      logging.error("A bus line identifier has to be provided")
      sys.exit("A bus line identifier has to be provided for action 'info_line'")
  elif args.action == "info_stops":
    logging.debug("x_client_id '%s' asking for bus stops information" % x_client_id)
    info_stops(busemtmad_service)
  elif args.action == "info_stop":
    if args.stop_id!=None:
      logging.debug("x_client_id '%s' asking for information for bus stop '%s'" %
                    (x_client_id, args.stop_id))
      info_stop(busemtmad_service, args.stop_id)
    else:
      logging.error("A bus stop identifier has to be provided")
      sys.exit("A bus stop identifier has to be provided for action 'info_stop'")
  elif args.action == "line_stops":
    if args.line_id!=None and args.direction!=None:
      logging.debug("x_client_id '%s' asking for stops of the line '%s' with direction '%s'" %
                    (x_client_id, args.line_id, args.direction))
      line_stops(busemtmad_service, args.line_id, args.direction)
    else:
      logging.error("A bus line identifier and direction have to be provided")
      sys.exit("A bus line identifier and direction have to be provided for action 'line_stops'")
  elif args.action == "issues":
    if args.stop_id!=None:
      logging.debug("x_client_id '%s' asking for issues for bus stop '%s'" %
                    (x_client_id, args.stop_id))
      issues(busemtmad_service, args.stop_id)
    else:
      logging.error("A bus stop identifier has to be provided")
      sys.exit("A bus stop has to be provided for action 'issues'")
  elif args.action == "buses_arrivals":
    if args.stop_id!=None:
      logging.debug("x_client_id '%s' asking for buses arrivals for bus stop '%s' and bus line '%s'" %
                    (x_client_id, args.stop_id, args.line_id))
      buses_arrivals(busemtmad_service, args.stop_id, args.line_id)
    else:
      logging.error("A bus stop identifier has to be provided")
      sys.exit("A bus stop has to be provided for action 'busesarrivals' at least")
else:
  logging.error("Unsuccessful login with x_client_id '%s%'" % x_client_id)
  sys.exit("Unsuccessful login with x_client_id '%s%'" % x_client_id)
