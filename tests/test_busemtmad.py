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
def infoLines(busemtmadService):
  todayString = datetime.today().strftime('%Y%m%d')
  infoLines = busemtmadService.infoLines(todayString)

  if infoLines!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoLines)
  else:
    print("The BusEMTMad service didn't return any data.")

def infoLine(busemtmadService, lineId):
  todayString = datetime.today().strftime('%Y%m%d')
  infoLine = busemtmadService.infoLine(lineId, todayString)

  if infoLine!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoLine)
  else:
    print("The BusEMTMad  service didn't return any data.")

def infoStops(busemtmadService):
  infoStops = busemtmadService.infoStops()

  if infoStops!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoStops)
  else:
    print("The BusEMTMad service didn't return any data.")

def infoStop(busemtmadService, stopId):
  infoStop = busemtmadService.infoStop(stopId)

  if infoStop!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoStop)
  else:
    print("The BusEMTMad  service didn't return any data.")

def issues(busemtmadService, stopId):
  issues = busemtmadService.issues(stopId)

  if issues!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(issues)
  else:
    print("The BusEMTMad  service didn't return any data.")

def busesArrivals(busemtmadService, stopId, lineId):
  if lineId!=None:
    busesArrivals = busemtmadService.busesArrivals(stopId, lineId)
  else:
    busesArrivals = busemtmadService.busesArrivals(stopId)

  if busesArrivals!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(busesArrivals)
  else:
    print("The BusEMTMad  service didn't return any data.")

# Setting up debuging level and debug file with environment variables
#
debugLevel = os.environ.get('MOBILITYLABS_DEBUGLEVEL',logging.WARN)
debugFile = os.environ.get('MOBILITYLABS_DEBUGFILE')

if debugFile==None:
  logging.basicConfig(level=debugLevel)
else:
  logging.basicConfig(filename=debugFile, filemode='w', level=debugLevel)

parser = argparse.ArgumentParser()
parser.add_argument("action", choices=['infoLines', 'infoLine', 'infoStops', 'infoStop', 'lineStops', 
                                       'issues', 'busesArrivals'],
                    help="what is going to be requested to the BusEMTMad service")
parser.add_argument("credentialsFile", help="path to the file with info to access the service")
parser.add_argument("-lid", "--lineId",
                    help="bus line identifier for actions 'infoLine', 'lineStops' and 'issues'; this argument is optional for action 'busesArrivals'")
parser.add_argument("-sid", "--stopId",
                    help="stop identifier for action 'infoStop' and 'busesArrivals'")
parser.add_argument("-dir", "--direction", choices=['1','2'],
                    help="direction to be considered to analyze line info for action 'linesStops'; 1 for start to end, 2 for end to start")
args = parser.parse_args()

# Read credentials to instantiate the class to use the service
#
credentials = configparser.ConfigParser()
credentials.read(args.credentialsFile)

XClientID = credentials['DEFAULT']['XClientID']
passkey = credentials['DEFAULT']['passkey']
busemtmadService = BusEMTMad(XClientID, passkey)
busemtmadService.logIn()

# Action dispatching if credentials logged the client into the service
#
if (busemtmadService.isLoggedIn()):
  if args.action == "infoLines":
    logging.debug("XClientID '%s' asking for lines information" % XClientID)
    infoLines(busemtmadService)
  elif args.action == "infoLine":
    if args.lineId!=None:
      logging.debug("XClientID '%s' asking for information for bus line '%s'" %
                    (XClientID, args.lineId))
      infoLine(busemtmadService, args.lineId)
    else:
      logging.error("A bus line identifier has to be provided")
      sys.exit("A bus line identifier has to be provided for action 'infoLine'")
  elif args.action == "infoStops":
    logging.debug("XClientID '%s' asking for bus stops information" % XClientID)
    infoStops(busemtmadService)
  elif args.action == "infoStop":
    if args.stopId!=None:
      logging.debug("XClientID '%s' asking for information for bus stop '%s'" %
                    (XClientID, args.stopId))
      infoStop(busemtmadService, args.stopId)
    else:
      logging.error("A bus stop identifier has to be provided")
      sys.exit("A bus stop has to be provided for action 'infoStop'")
  elif args.action == "issues":
    if args.stopId!=None:
      logging.debug("XClientID '%s' asking for issues for bus stop '%s'" %
                    (XClientID, args.stopId))
      issues(busemtmadService, args.stopId)
    else:
      logging.error("A bus stop identifier has to be provided")
      sys.exit("A bus stop has to be provided for action 'issues'")
  elif args.action == "busesArrivals":
    if args.stopId!=None:
      logging.debug("XClientID '%s' asking for buses arrivals for bus stop '%s' and bus line '%s'" %
                    (XClientID, args.stopId, args.lineId))
      busesArrivals(busemtmadService, args.stopId, args.lineId)
    else:
      logging.error("A bus stop identifier has to be provided")
      sys.exit("A bus stop has to be provided for action 'busesarrivals' at least")
else:
  logging.error("Unsuccessful login with XClientID '%s%'" % XClientId)
  sys.exit("Unsuccessful login with XClientID '%s%'" % XClientId)
