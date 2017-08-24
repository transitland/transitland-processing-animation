import time
import urllib
import urllib2
import json

class TransitlandRequest(object):
  """Simple transitland API interface, with rate limits."""
  last_request_time = 0.0 # time of last request

  def __init__(self, host='https://transit.land', apikey=None, ratelimit=8, retrylimit=5):
    self.host = host
    self.apikey = apikey
    self.ratelimit = ratelimit
    self.retrylimit = retrylimit

  def wait_time(self):
    now = time.time()
    wait_time = (1.0 / self.ratelimit) - (now - self.last_request_time)
    # print "ratelimit: ", self.ratelimit, " /s: ", (1.0 / self.ratelimit)
    # print "last_request_time: ", self.last_request_time
    # print "now: ", now
    # print "dt: ", (now - self.last_request_time)
    # print "wait_time: ", wait_time
    if wait_time > 0:
      time.sleep(wait_time)
    self.last_request_time = now

  def _request(self, uri, retries=0):
    print uri
    success = False
    data = {}
    while not success:
      self.wait_time()
      try:
        req = urllib2.Request(uri)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req)
        if response.getcode() >= 400:
          raise StandardError('http error: %s'%(response.getcode()))
        else:
          success = True
          data = json.loads(response.read())
      except StandardError as e:
        retries += 1
        if retries > self.retrylimit:
          raise e
        print "retry %s / %s: %s"%(retries, self.retrylimit, e)
    return data

  def request(self, endpoint, **data):
    """Request with JSON response."""
    # Create uri
    data = data or {}
    if self.apikey:
      data['apikey'] = self.apikey

    next_uri = '%s/api/v1/%s?%s'%(self.host, endpoint, urllib.urlencode(data).replace("%7E","~")) # to fix o-dr5-nj~transit

    # Pagination
    while next_uri:
        data = self._request(next_uri)
        meta = data.get('meta', {})
        next_uri = meta.get('next')
        # Temporary fix for pagination missing apikey
        if next_uri and self.apikey and ('apikey=' not in next_uri):
          next_uri = "%s&apikey=%s"%(next_uri, self.apikey)
        # transitland responses will have one main key that isn't "meta"
        main_key = (set(data.keys()) - set(['meta'])).pop().replace("%7E","~") # to fix o-dr5-nj~transit
        for item in data[main_key]:
            yield item
