# -*- coding: UTF-8 -*-

import requests
from io import BytesIO
from PIL import Image, ImageDraw,ImageFont
import urllib, base64
import tools
import evnsetting
from datetime import *

def init(key_str, endpoint_str):
  evnsetting.setKey(key_str)
  evnsetting.setEndPoint(endpoint_str)

def getHeader():
  headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': evnsetting.getKey(),
  }
  return headers

def getParams(face_id='true',face_landmarks='false',attr=''):
  params = urllib.urlencode({
    # Request parameters
    'returnFaceId': face_id,
    'returnFaceLandmarks': face_landmarks,
    'returnFaceAttributes': attr,
  })
  return params

def getNullParams(face_id='true',face_landmarks='false',attr=''):
  params = urllib.urlencode({
  })
  return params

def createPersonGroup(group_name):
  print 'create person group'
  in_params = getNullParams()
  in_headers = getHeader()
  response = requests.request("PUT", evnsetting.getEndPoint()+'persongroups/'+group_name, 
                              params=in_params, 
                              json={"name": group_name}, 
                              data=None, 
                              headers=in_headers)
  result = None
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  if response.text:
    result = response.json()
  else:
    result = {}
  return result


def createPerson(group_name, person_name):
  print 'create person: ' + person_name
  in_params = getNullParams()
  in_headers = getHeader()
  response = requests.request("POST", evnsetting.getEndPoint()+'persongroups/'+group_name+'/persons', 
                              params=in_params, 
                              json={"name": person_name}, 
                              data=None, 
                              headers=in_headers)
  result = None
    # `person_group.train` return 202 status code for success.
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  if response.text:
    result = response.json()
    return result['personId']
  else:
    result = {}
    return 'None'
  
def addFace(group_name, person_id, img_url):
  print person_id
  print img_url
  in_params = getNullParams()
  in_headers = getHeader()
  print 'add a face from ' + img_url + ' for ' + person_id + ' in ' + group_name
  response = requests.request("POST", evnsetting.getEndPoint()+'persongroups/'+group_name+'/persons/'+person_id+'/persistedFaces', 
                              params=in_params, 
                              json={'url': img_url}, 
                              data=None, 
                              headers=in_headers)
  result = None
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  print response.json()
  if response.text:
    result = response.json()
    return result['persistedFaceId']
  else:
    result = {}
    return 'None'

def trainPersonFace(group_name):
  print 'train one person group'
  in_params = getNullParams()
  in_headers = getHeader()
  response = requests.request("POST", evnsetting.getEndPoint()+'persongroups/'+group_name+'/train', 
                              params=in_params, 
                              json=None, 
                              data=None, 
                              headers=in_headers)
  result = None
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  if response.text:
    result = response.json()
  else:
    result = {}

  response = requests.request("GET", evnsetting.getEndPoint()+'persongroups/'+group_name+'/training', 
                              params=None, 
                              json=None, 
                              data=None, 
                              headers=in_headers)
  result = None
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  if response.text:
    result = response.json()
    return result['status']
  else:
    result = None
    return 'None'

def detectFace(in_params, in_headers, img_url):
  print 'detect one face'
  response = requests.request("POST", evnsetting.getEndPoint()+'detect', 
                              params=in_params, 
                              json={'url': img_url}, 
                              data=None, 
                              headers=in_headers)
  faces = None
    # `person_group.train` return 202 status code for success.
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  if response.text:
    faces = response.json()
  else:
    faces = {}

  face_list=[]
  print faces
  for face in faces:
    faceid = face['faceId']
    face_list.append(str(faceid))
  #print face_list
  return (faces,face_list)

def deletePersonGroup(in_headers, group_name):
  #print in_headers
  response = requests.request("DELETE", evnsetting.getEndPoint()+'persongroups/'+group_name, 
                              params=None, 
                              json=None, 
                              data=None, 
                              headers=in_headers)
  identify_result = None
    # `person_group.train` return 202 status code for success.
  if response.status_code not in (200, 202):
    try:
      error_msg = response.json()['error']
    except:
      raise CognitiveFaceException(response.status_code,response.status_code, response.text)
      raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
  print response


def identifyFace(img_url, group_name):
  print 'identify one face'
  in_params = getParams(attr='age,emotion')
  in_headers = getHeader()
  face_result = detectFace(in_params, in_headers, img_url)
  print face_result
  face_result_len = len(face_result[1])
  identify_result = []
  #print face_result_len
  for i in range(face_result_len / 10 + 1):    
    if i+10 > face_result_len:
      last_index = face_result_len
    else:
      last_index = i + 10
    if i * 10 == last_index:
      break
    #print 'start:' + str(i*10) + ' end:' + str(last_index)
    #last_index = i+10 > face_result_len ? face_result_len : i+10
    response = requests.request("POST", evnsetting.getEndPoint()+'identify', 
                                params=None, 
                                json={'faceIds': face_result[1][i*10:last_index], 'personGroupId':group_name}, 
                                data=None, 
                                headers=in_headers)
    
    # `person_group.train` return 202 status code for success.
    if response.status_code not in (200, 202):
      try:
        error_msg = response.json()['error']
      except:
        raise CognitiveFaceException(response.status_code,response.status_code, response.text)
        raise CognitiveFaceException(response.status_code,
                                     error_msg.get('code'),
                                     error_msg.get('message'))
    if response.text:
      for item in response.json():       
        identify_result.append(item)
    else:
      identify_result = []

  #print identify_result
  name_list= []
  for person in identify_result:
    if person['candidates'] == []:
      name_list.append('unknown')
      continue
    targetid = person['candidates'][0]['personId']
    response = requests.request("GET", evnsetting.getEndPoint()+'persongroups/'+group_name+'/persons/'+targetid, 
                                params=None, 
                                json=None, 
                                data=None, 
                                headers=in_headers)
    person_result = None
    person_result = response.json()
    print person_result['name']
    name_list.append(person_result['name'])


  img_response = requests.get(img_url)
  target_img = Image.open(BytesIO(img_response.content))

#For each face returned use the face rectangle and draw a red box.
  draw = ImageDraw.Draw(target_img)
  name_index = 0
  for face in face_result[0]:
    draw.rectangle(tools.getRectangle(face), outline='red')
    Font1 = ImageFont.truetype("C:\Windows\Fonts\consola.ttf",size=32)
    Font2 = ImageFont.truetype("C:\Windows\Fonts\consola.ttf",size=80)
    happy_ratio =  face['faceAttributes']['emotion']['happiness'] * 100
    draw.text(tools.getBottomPos(face),'H:'+str(happy_ratio),fill = (255,0,0),font=Font1)
    l_left, l_top = tools.getNamePos(face)
    if(l_left + 400 > target_img.width):
      l_left = l_left - 100
    draw.text((l_left, l_top),name_list[name_index]+' A:'+str(face['faceAttributes']['age']),fill = (255,0,0),font=Font1)
    name_index += 1
  draw.text((target_img.width-2300,target_img.height- 120 ),"Microsoft Azure AI: give you a memento. " + str(date.today()),fill = (50,205,50),font=Font2)

#Display the image in the users default image browser.
  target_img.show()
  #target_img.save('result.jpg')
  #print img_url
  target_img.save(img_url.split('/')[-1])

#person_group = 'facegroupnew1'

#init('4b7579dc7a404a97a2d8bd48d5790d','https://eastasia.api.cognitive.microsoft.com/face/v1.0/')
#identifyFace('https://gusufaceapitest.blob.core.windows.net/vanke-new-group/group2.JPG',person_group)
#deletePersonGroup(getHeader(),'facegroup3')


#identifyFace(getParams(attr='age'),getHeader(), 'https://gusufaceapitest.blob.core.windows.net/pic1/xt3.jpg','facegroup1')

#identifyFace(getParams(attr='age'), getHeader(), 'https://gusufaceapitest.blob.core.windows.net/facelab/team5.jpg', 'gusutestgroup1')