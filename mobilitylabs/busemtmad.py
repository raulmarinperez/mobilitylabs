from mobilitylabs.core import MobilityLabs
import time
import logging
import requests

class BusEMTMad(MobilityLabs):

  def __init__(self, XClientId, passKey):
    MobilityLabs.__init__(self, XClientId, passKey)

  def infoLines(self, dateref):
    url = "%s/transport/busemtmad/lines/info/%s/" % (self.MLURL, dateref)
    headers = {'accessToken': self._accessToken}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of lines retrieved: %s" % resp.json()['data'])
      return resp.json()['data']
      
    logging.error("Unable to log in with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None

  def infoLine(self, lineId, dateref):
    url = "%s/transport/busemtmad/lines/%s/info/%s/" % \
          (self.MLURL, lineId, dateref)
    headers = {'accessToken': self._accessToken}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      logging.debug("Info of line '%s': %s" % \
                    (lineId, resp.json()['data']))
      return resp.json()['data']

    logging.error("Unable to log in with code '%s' and message: %s" %
                  (resp.status_code, resp.reason))
    return None
