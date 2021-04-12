from mobilitylabs.bicimad import BiciMad
import configparser
import argparse
import logging
import pprint
import sys
import os

# Auxiliary functions
#
def info_bike_stations(bicimad_service):
  info_bike_stations = bicimad_service.info_bike_stations()

  if info_bike_stations!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_bike_stations)
  else:
    print("The BiciMAD GO service didn't return any data.")

def info_bike_station(bicimad_service, bike_station_id):
  info_bike_station = bicimad_service.info_bike_station(bike_station_id)

  if info_bike_station!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_bike_station)
  else:
    print("The BiciMAD GO service didn't return any data.")

def info_bikes(bicimad_service):
  info_bikes = bicimad_service.info_bikes()

  if info_bikes!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_bikes)
  else:
    print("The BiciMAD GO service didn't return any data.")

def info_bike(bicimad_service, bike_id):
  info_bike= bicimad_service.info_bike(bike_id)

  if info_bike!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_bike)
  else:
    print("The BiciMAD GO service didn't return any data.")

# Setting up debuging level and debug file with environment variables
#
debug_level = os.environ.get('MOBILITYLABS_DEBUGLEVEL',logging.WARN)
debug_file = os.environ.get('MOBILITYLABS_DEBUGFILE')

if debug_file==None:
  logging.basicConfig(level=debug_level)
else:
  logging.basicConfig(filename=debug_file, filemode='w', level=debug_level)

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['info_bike_stations', 'info_bike_station', 'info_bikes', 'info_bike'],
                    help="what is going to be requested to the BiciMAD GO service")
parser.add_argument("credentials_file", help="path to the file with info to access the service")
parser.add_argument("-sid", "--bike_station_id",
                    help="bike station identifier for action 'info_bike_station'")
parser.add_argument("-bid", "--bike_id",
                    help="bike identifier for action 'info_bike'")
args = parser.parse_args()

# Read credentials to instantiate the class to use the service
#
credentials = configparser.ConfigParser()
credentials.read(args.credentials_file)

x_client_id = credentials['DEFAULT']['x_client_id']
pass_key = credentials['DEFAULT']['pass_key']
bicimad_service = BiciMad(x_client_id, pass_key)
bicimad_service.log_in()

# Action dispatching if credentials logged the client into the service
#
if (bicimad_service.is_logged_in()):
  if args.action == "info_bike_stations":
    logging.debug("x_client_id '%s' asking for bike stations information" % x_client_id)
    info_bike_stations(bicimad_service)
  elif args.action == "info_bike_station":
    if args.bike_station_id!=None:
      logging.debug("x_client_id '%s' asking for information for bike station '%s'" %
                    (x_client_id, args.bike_station_id))
      info_bike_station(bicimad_service, args.bike_station_id)
    else:
      logging.error("A bike station identifier has to be provided")
      sys.exit("A bike station identifier has to be provided for action 'info_bike_station'")
  elif args.action == "info_bikes":
    logging.debug("x_client_id '%s' asking for bikes information" % x_client_id)
    info_bikes(bicimad_service)
  elif args.action == "info_bike":
    if args.bike_id!=None:
      logging.debug("x_client_id '%s' asking for information for bike '%s'" %
                    (x_client_id, args.bike_id))
      info_bike(bicimad_service, args.bike_id)
    else:
      logging.error("A bike identifier has to be provided")
      sys.exit("A bike identifier has to be provided for action 'info_bike'")
  else:
    logging.error("Unsuccessful login with x_client_id '%s%'" % XClientId)
    sys.exit("Unsuccessful login with x_client_id '%s%'" % XClientId)

