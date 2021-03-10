import time
import logging
import requests

class MobilityLabs:

  MLURL = "https://openapi.emtmadrid.es/v1"
  _XClientId = ""
  _passKey = ""
  _accessToken = ""
  _tokenSecExpiration = 0
  _loggedIn = False

  def __init__(self, XClientId, passKey):
    logging.basicConfig(level=logging.DEBUG)
    self._XClientId = XClientId
    self._passKey = passKey
    logging.debug("New MobilityLabs instance for X-ClientId '%s'" % self._XClientId)

  def isLoggedIn(self):
    return self._logged_in

  def logIn(self):
    url = "%s/mobilitylabs/user/login/" % self.MLURL
    headers = {'X-ClientId': self._XClientId, 'passKey': self._passKey}
    resp = requests.get(url, headers=headers)

    if resp.status_code == 200:
      response = resp.json()
      self._accessToken = response['data'][0]['accessToken']
      self._tokenSecExpiration = time.time() + response['data'][0]['tokenSecExpiration']
      self._loggedIn = True
      logging.debug("Token '%s' created and will expire %d seconds" %
                    (self._accessToken, response['data'][0]['tokenSecExpiration']))
      return True

    logging.error("Unable to log in with code '%s' and message: %s" % 
                  (resp.status_code, resp.reason))
    return False
 
