import cv2 as cv
import face_recognition
import pickle
import os


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("D:\projects\FaceRecognition-Minor_Project\Service_Account_Key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL':"https://face-recognition-78e82-default-rtdb.firebaseio.com/",
    'storageBucket':"face-recognition-78e82.appspot.com"
})

# IMPORTING THE IMAGES INTO A LIST
folderPath = "D:\projects\FaceRecognition-Minor_Project\Images"
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentID = []
for path in pathList:
    imgList.append(cv.imread(os.path.join(folderPath,path)))
    studentID.append(os.path.splitext(path)[0])

# ____________SENDING DATA TO IMAGES FIREBASE__________________
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # print(path)
    # print(os.path.splitext(path)[0])
# print(len(imgModeList))
print(studentID)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

print("Encoding Started...")
encodeListKnown = findEncodings(imgList)
encodeList_Known_WithIDs = [encodeListKnown,studentID ]
print("Encoding Ended...")
  
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeList_Known_WithIDs, file)
file.close()
print("file saved")

 