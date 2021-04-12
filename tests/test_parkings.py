from mobilitylabs.parkingemtmad import ParkingEMTMad
import configparser
import argparse
import logging
import pprint
import sys
import os

# Auxiliary functions
#
def info_parkings(parking_service):
  info_parkings = parking_service.info_parkings()

  if info_parkings!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_parkings)
  else:
    print("The ParkingEMTMad service didn't return any data.")

def info_parking(parking_service, parking_id):
  info_parking = parking_service.info_parking(parking_id)

  if info_parking!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(info_parking)
  else:
    print("The ParkingEMTMad service didn't return any data.")

def availability(parking_service):
  availability = parking_service.availability()

  if availability!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(availability)
  else:
    print("The ParkingEMTMad service didn't return any data.")

# Setting up debuging level and debug file with environment variables
#
debug_level = os.environ.get('MOBILITYLABS_DEBUGLEVEL',logging.WARN)
debug_file = os.environ.get('MOBILITYLABS_DEBUGFILE')

if debug_file==None:
  logging.basicConfig(level=debug_level)
else:
  logging.basicConfig(filename=debug_file, filemode='w', level=debug_level)

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['info_parkings', 'info_parking', 'availability'],
                    help="what is going to be requested to the ParkingEMTMad service")
parser.add_argument("credentials_file", help="path to the file with info to access the service")
parser.add_argument("-id", "--parking_id", 
                    help="parking area identifier for action 'info_parking'")
args = parser.parse_args()

# Read credentials to instantiate the class to use the service
#
credentials = configparser.ConfigParser()
credentials.read(args.credentials_file)

x_client_id = credentials['DEFAULT']['x_client_id']
pass_key = credentials['DEFAULT']['pass_key']
parking_service = ParkingEMTMad(x_client_id, pass_key)
parking_service.log_in()

# Action dispatching if credentials logged the client into the service
#
if (parking_service.is_logged_in()):
  if args.action == "info_parkings":
    logging.debug("x_client_id '%s' asking for parking areas information" % x_client_id)
    info_parkings(parking_service)
  elif args.action == "info_parking":
    if args.parking_id!=None:
      logging.debug("x_client_id '%s' asking for information for parking area '%s'" % 
                    (x_client_id, args.parking_id))
      info_parking(parking_service, args.parking_id)
    else:
      logging.error("A parking area identifier has to be provided")
      sys.exit("A parking area identifier has to be provided for action 'info_parking'")
  elif args.action == "availability":
    logging.debug("x_client_id '%s' asking for availability in parking areas" % x_client_id)
    availability(parking_service)
else:
  logging.error("Unsuccessful login with x_client_id '%s%'" % x_client_id)
  sys.exit("Unsuccessful login with x_client_id '%s%'" % x_client_id)
