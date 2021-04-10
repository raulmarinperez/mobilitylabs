#!/usr/bin/python3
from mobilitylabs.busemtmad import BusEMTMad
import configparser
import argparse
import logging
import pprint
import sys
import os

#line523Issues = busemtmad.incidents("523")
#busArriva316Line147 = busemtmad.busesarrivals("316","147")
#busArriva316Line147 = busemtmad.busesarrivals("316")
#infoStop316 = busemtmad.infoStop("316")

# Auxiliary functions
#
def infoLines(busemtmadService):
  infoLines = busemtmadService.infoLines("20210410")

  if infoLines!=None:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(infoLines)
  else:
    print("The BusEMTMad service didn't return any data.")

def infoLine(busemtmadService, lineId):
  infoLine = busemtmadService.infoLine(lineId, "20210410")

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
                                       'incidents', 'busesarrivales'],
                    help="what is going to be requested to the BusEMTMad service")
parser.add_argument("credentialsFile", help="path to the file with info to access the service")
parser.add_argument("-lid", "--lineId",
                    help="bus line identifier for actions 'infoLine', 'lineStops' and 'incidents'; this argument is optional for action 'busesarrivales'")
parser.add_argument("-sid", "--stopId",
                    help="stop identifier for action 'infoStop' and 'busesarrivales'")
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
  else:
    logging.error("Unsuccessful login with XClientID '%s%'" % XClientId)
    sys.exit("Unsuccessful login with XClientID '%s%'" % XClientId)
