import tools
import evnsetting
import facemodule
import sys

facemodule.init('221c68c41a404ff2a9f30e9a667f4f78','https://facetestlab.cognitiveservices.azure.com/face/v1.0/')
upload_result = tools.uploadFiles('C:\Users\yimao\Pictures\/singleperson','face')
person_name_list = upload_result[2]
file_list = upload_result[1]
img_base_url = upload_result[0]
print person_name_list
person_group = 'xtem'
person_name_id_dict = {}
facemodule.createPersonGroup(person_group)
for person_name in person_name_list:
  person_id = facemodule.createPerson(person_group,person_name)
  person_name_id_dict[person_name] = person_id

print person_name_id_dict

for img_file in file_list:
  persone_current_name = tools.getPersonName(img_file)
  persisted_face_id = facemodule.addFace(person_group,person_name_id_dict[persone_current_name],img_base_url+img_file)
  print persisted_face_id

facemodule.trainPersonFace(person_group)
upload_path = tools.uploadFile('C:\Users\yimao\Pictures\/team1\groupie1.jpg', 'groupie1.jpg', 'face')
print upload_path[0]
facemodule.identifyFace(upload_path[0],person_group)
#identifyFace(getParams(attr='age'), getHeader(), 'https://gusufaceapitest.blob.core.windows.net/facelab/team5.jpg', 'gusutestgroup1')