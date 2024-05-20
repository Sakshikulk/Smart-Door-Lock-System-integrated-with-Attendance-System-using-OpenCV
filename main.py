import cv2 as cv
import os 
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime



import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage



from controller import rotateServo
import time


cred = credentials.Certificate("D:\projects\FaceRecognition-Minor_Project\Service_Account_Key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL':"https://face-recognition-78e82-default-rtdb.firebaseio.com/",
    'storageBucket':"face-recognition-78e82.appspot.com"
})

bucket=storage.bucket()


cap = cv.VideoCapture(0)
cap.set(3,668)
cap.set(4,569)

imgBack = cv.imread("D:\projects\FaceRecognition-Minor_Project\webcam+Blank.png")

# IMPORTING THE MODE IMAGES INTO A LIST
folderModePath = "D:\projects\FaceRecognition-Minor_Project\Modes"
modePath = os.listdir(folderModePath)
imgModeList = []
for path in modePath:
    imgModeList.append(cv.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))

# LOAD THE ENCODING FILE
print("Loading encode file...")
file = open("EncodeFile.p", 'rb')
encodeList_Known_WithIDs = pickle.load(file)
file.close()
encodeListKnown,studentID = encodeList_Known_WithIDs
# print(studentID)
print("Encode file loaded")


# _____________IMAGE UPDATING AFTER FACE DETECTION__________________
modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, frame = cap.read()

    # _________________IMAGE RESIZING__________ 
    imgS = cv.resize(frame,(0,0), None, 0.25, 0.25 )
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    # ___________________FEEDING TO FACE RECOGNITION SYSTEM_______________
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    # read after img background change

    frame_resized = cv.resize(frame, (668, 569))
    imgBack[104:104+569, 47:47+668] = frame_resized

    imgModeList[modeType] = cv.resize(imgModeList[modeType], (521,641) )
    imgBack[34:34+641, 750:750+521] = imgModeList[modeType]
    

    # ___________FACE RECOGNITION_______________
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("Matches", matches)
            # print("face-Diatances", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index:",matchIndex)

            if matches[matchIndex]:
                # print("Known face is detected!")
                # print("Id is :",studentID[matchIndex])

                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4 ,x2*4 ,y2*4 ,x1*4
                bbox = 47+x1, 104+y1, x2-x1, y2-y1
                imgBack = cvzone.cornerRect(imgBack, bbox, rt = 0)

                id = studentID[matchIndex]

                if counter==0:
                    counter = 1
                    modeType = 1
            
        if counter!=0:
            
            if counter == 1:  # download the data for only first frame only

                # download the data and show it
                studentInfo = db.reference(f'Students/{id}').get() # download
                print(studentInfo)

                # updating the attendance

                datetimeObj = datetime.strptime(studentInfo["Last_Time_Entered"],
                                            "%Y-%m-%d %H:%M:%S")
                secsElapsed = (datetime.now()-datetimeObj).total_seconds()
                print(secsElapsed)

                if secsElapsed>30:
                    ref = db.reference(f'Students/{id}')
                    studentInfo["Total_Attendance"] +=1
                    ref.child("Total_Attendance").set(studentInfo["Total_Attendance"])
                    ref.child("Last_Time_Entered").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                
                else:
                    modeType = 3
                    counter = 0
                    rotateServo(8,90)
                    time.sleep(5)
                    # print("QWERTYUIDFVGBHNJ")
                    rotateServo(8,0)
                    time.sleep(5)
                    imgModeList[modeType] = cv.resize(imgModeList[modeType], (521,641) )
                    imgBack[34:34+641, 750:750+521] = imgModeList[modeType]
                    # continue
                
            if modeType!=3:       

                if 10<counter<15:
                    modeType = 2
                    rotateServo(8,90)
                    time.sleep(5)
                    # print("QWERTYUIDFVGBHNJ")
                    rotateServo(8,0)
                    time.sleep(5)
                    # continue




                imgModeList[modeType] = cv.resize(imgModeList[modeType], (521,641) )
                imgBack[34:34+641, 750:750+521] = imgModeList[modeType]


                if counter<=10:   
                    # DISPLAYING THOSE VALUES WHICH SHOULD BE DISPLAYED IN ALL THE FRAMES
                    # displaying name
                    (w,h) , _ = cv.getTextSize(studentInfo["NAME"], cv.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (1322 - w)//2
                    cv.putText(imgBack, str(studentInfo["NAME"]),(395+offset, 390), cv.FONT_HERSHEY_COMPLEX, 0.7, (50,50,50),1 )

                    # displaying reg no
                    cv.putText(imgBack, str(studentInfo["Registration_number"]),(520+offset, 425), cv.FONT_HERSHEY_COMPLEX, 0.7, (50,50,50),1 )

                    # displaying attendance
                    cv.putText(imgBack, str(studentInfo["Total_Attendance"]),(563+offset, 458), cv.FONT_HERSHEY_COMPLEX, 0.7, (50,50,50),1 )

            
                counter += 1

                if counter>=15:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgModeList[modeType] = cv.resize(imgModeList[modeType], (521,641) )
                    imgBack[34:34+641, 750:750+521] = imgModeList[modeType]
    else:
         modeType = 0
         counter = 0           

    # cv.imshow("webcam", frame)
    # cv.imshow("img", imgBack)

    cv.imshow("faceVideo", imgBack)
    # cv.waitKey(1)

    if cv.waitKey(20) & 0xFF==ord("d"): # BREAK IF FRAME IS NOT DETECTED OR D IS PRESSED
        break
    
cap.release()
cv.destroyAllWindows()
