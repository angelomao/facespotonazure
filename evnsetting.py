global KEY
KEY = 'None'
global ENDPOINT
ENDPOINT = 'None'

def getKey():
  global KEY
  return  KEY

def getEndPoint():
  global ENDPOINT
  return  ENDPOINT

def setKey(key_str):
  global KEY 
  KEY = key_str
  print KEY

def setEndPoint(endpoint_str):
  global ENDPOINT 
  ENDPOINT = endpoint_str
  print  ENDPOINT