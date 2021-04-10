#!/usr/bin/python3
from mobilitylabs.bicimad import BiciMad
import configparser
import argparse
import logging
import pprint
import sys
import os

# Auxiliary functions
#
def infoBikeStations(bicimadService):
  infoBikeStations = bicimadService.infoBikeStations()

  if infoBikeStations!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoBikeStations)
  else:
    print("The BiciMAD GO service didn't return any data.")

def infoBikeStation(bicimadService, bikeStationId):
  infoBikeStation = bicimadService.infoBikeStation(bikeStationId)

  if infoBikeStation!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoBikeStation)
  else:
    print("The BiciMAD GO service didn't return any data.")

def infoBikes(bicimadService):
  infoBikes = bicimadService.infoBikes()

  if infoBikes!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoBikes)
  else:
    print("The BiciMAD GO service didn't return any data.")

def infoBike(bicimadService, bikeId):
  infoBike= bicimadService.infoBike(bikeId)

  if infoBike!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoBike)
  else:
    print("The BiciMAD GO service didn't return any data.")

# Setting up debuging level and debug file with environment variables
#
debugLevel = os.environ.get('MOBILITYLABS_DEBUGLEVEL',logging.WARN)
debugFile = os.environ.get('MOBILITYLABS_DEBUGFILE')

if debugFile==None:
  logging.basicConfig(level=debugLevel)
else:
  logging.basicConfig(filename=debugFile, filemode='w', level=debugLevel)

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['infoBikeStations', 'infoBikeStation', 'infoBikes', 'infoBike'],
                    help="what is going to be requested to the BiciMAD GO service")
parser.add_argument("credentialsFile", help="path to the file with info to access the service")
parser.add_argument("-sid", "--bikeStationId",
                    help="bike station identifier for action 'infoBikeStation'")
parser.add_argument("-bid", "--bikeId",
                    help="bike identifier for action 'infoBike'")
args = parser.parse_args()

# Read credentials to instantiate the class to use the service
#
credentials = configparser.ConfigParser()
credentials.read(args.credentialsFile)

XClientID = credentials['DEFAULT']['XClientID']
passkey = credentials['DEFAULT']['passkey']
bicimadService = BiciMad(XClientID, passkey)
bicimadService.logIn()

# Action dispatching if credentials logged the client into the service
#
if (bicimadService.isLoggedIn()):
  if args.action == "infoBikeStations":
    logging.debug("XClientID '%s' asking for bike stations information" % XClientID)
    infoBikeStations(bicimadService)
  elif args.action == "infoBikeStation":
    if args.bikeStationId!=None:
      logging.debug("XClientID '%s' asking for information for bike station '%s'" %
                    (XClientID, args.bikeStationId))
      infoBikeStation(bicimadService, args.bikeStationId)
    else:
      logging.error("A bike station identifier has to be provided")
      sys.exit("A bike station identifier has to be provided for action 'infoBikeStation'")
  elif args.action == "infoBikes":
    logging.debug("XClientID '%s' asking for bikes information" % XClientID)
    infoBikes(bicimadService)
  elif args.action == "infoBike":
    if args.bikeId!=None:
      logging.debug("XClientID '%s' asking for information for bike '%s'" %
                    (XClientID, args.bikeId))
      infoBike(bicimadService, args.bikeId)
    else:
      logging.error("A bike identifier has to be provided")
      sys.exit("A bike identifier has to be provided for action 'infoBike'")
  else:
    logging.error("Unsuccessful login with XClientID '%s%'" % XClientId)
    sys.exit("Unsuccessful login with XClientID '%s%'" % XClientId)

