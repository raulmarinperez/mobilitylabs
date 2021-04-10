#!/usr/bin/python3
from mobilitylabs.parkingemtmad import ParkingEMTMad
import configparser
import argparse
import logging
import pprint
import sys
import os

# Auxiliary functions
#
def infoParkings(parkingService):
  infoParkings = parkingService.infoParkings()

  if infoParkings!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoParkings)
  else:
    print("The ParkingEMTMad service didn't return any data.")

def infoParking(parkingService, parkingId):
  infoParking = parkingService.infoParking(parkingId)

  if infoParking!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoParking)
  else:
    print("The ParkingEMTMad service didn't return any data.")

def availability(parkingService):
  availability = parkingService.availability()

  if availability!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(availability)
  else:
    print("The ParkingEMTMad service didn't return any data.")

# Setting up debuging level and debug file with environment variables
#
debugLevel = os.environ.get('MOBILITYLABS_DEBUGLEVEL',logging.WARN)
debugFile = os.environ.get('MOBILITYLABS_DEBUGFILE')

if debugFile==None:
  logging.basicConfig(level=debugLevel)
else:
  logging.basicConfig(filename=debugFile, filemode='w', level=debugLevel)

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['infoParkings', 'infoParking', 'availability'],
                    help="what is going to be requested to the ParkingEMTMad service")
parser.add_argument("credentialsFile", help="path to the file with info to access the service")
parser.add_argument("-id", "--parkingId", 
                    help="parking area identifier for action 'infoParking'")
args = parser.parse_args()

# Read credentials to instantiate the class to use the service
#
credentials = configparser.ConfigParser()
credentials.read(args.credentialsFile)

XClientID = credentials['DEFAULT']['XClientID']
passkey = credentials['DEFAULT']['passkey']
parkingService = ParkingEMTMad(XClientID, passkey)
parkingService.logIn()

# Action dispatching if credentials logged the client into the service
#
if (parkingService.isLoggedIn()):
  if args.action == "infoParkings":
    logging.debug("XClientID '%s' asking for parking areas information" % XClientID)
    infoParkings(parkingService)
  elif args.action == "infoParking":
    if args.parkingId!=None:
      logging.debug("XClientID '%s' asking for information for parking area '%s'" % 
                    (XClientID, args.parkingId))
      infoParking(parkingService, args.parkingId)
    else:
      logging.error("A parking area identifier has to be provided")
      sys.exit("A parking area identifier has to be provided for action 'infoParking'")
  elif args.action == "availability":
    logging.debug("XClientID '%s' asking for availability in parking areas" % XClientID)
    availability(parkingService)
else:
  logging.error("Unsuccessful login with XClientID '%s%'" % XClientId)
  sys.exit("Unsuccessful login with XClientID '%s%'" % XClientId)
