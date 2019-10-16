import os
import re
from azure.storage.blob import BlockBlobService, PublicAccess

def getPersonName(filename):
  if not filename[0].isalpha():
    return 'NoOne' 
  m = re.search('\d',filename)
  if m:
    return filename[:m.start()]
  else:
    return 'NoOne'

def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

def getNamePos(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    width = rect['width'] / 4
    return((left-width,top-40))


def getBottomPos(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = top + rect['height']
    right = left + rect['width']
    return((left+10,bottom+10))
    
def uploadFiles(file_path, container_name):
  block_blob_service = BlockBlobService(account_name='facetestlab', account_key='18d1Xq+BNjLTlAzAGikQf75JE/LX2UFnCcPpxfobm7RwHpZ9qViaAj/n/1qWdxfM7Yn/GP3Q7HpVsydNxUvAxA==') 
  files = os.listdir(file_path)
  name_list= []
  for child_file in files:
    person_name = getPersonName(child_file)
    if person_name == 'NoOne':
      continue
    else:
      if person_name not in name_list:
        name_list.append(person_name)
    full_path_to_file = file_path + '\/' + child_file
    block_blob_service.create_blob_from_path(container_name, child_file, full_path_to_file)
  access_link = 'https://facetestlab.blob.core.windows.net/'+container_name+'/'
  return(access_link, files, name_list)

def uploadFile(file_full_path, file_name, container_name):
  block_blob_service = BlockBlobService(account_name='facetestlab', account_key='18d1Xq+BNjLTlAzAGikQf75JE/LX2UFnCcPpxfobm7RwHpZ9qViaAj/n/1qWdxfM7Yn/GP3Q7HpVsydNxUvAxA==') 
  block_blob_service.create_blob_from_path(container_name, file_name, file_full_path)
  access_link = 'https://facetestlab.blob.core.windows.net/face/'+file_name
  return(access_link, file_name)
#print uploadFiles('C:\Users\gusu\Pictures\picfolder1','pic1')