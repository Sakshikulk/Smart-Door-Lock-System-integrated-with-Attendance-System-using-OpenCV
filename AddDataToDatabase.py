import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("D:\projects\FaceRecognition-Minor_Project\Service_Account_Key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL':"https://face-recognition-78e82-default-rtdb.firebaseio.com/"

})

ref = db.reference("Students")

data = {
        "1":
        {
            "NAME": "Sakshi Kulkarni",
            "Registration_number": "219311147", 
            "Last_Time_Entered": "2024-04-3 00:54:34" ,
            "Total_Attendance" : 0
        } ,
        "2":
        {
            "NAME": "Sanjay Kulkarni",
            "Registration_number": "219311148", 
            "Last_Time_Entered": "2024-04-3 00:54:34" , 
            "Total_Attendance" : 0

        } ,
        "3":
        {
            "NAME": "Sundar Pichai",
            "Registration_number": "219311149", 
            "Last_Time_Entered": "2024-04-3 00:54:34" ,
            "Total_Attendance" : 0

        }

}

for key,value in data.items():
    ref.child(key).set(value)