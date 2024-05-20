# Smart-Door-Lock-System-integrated-with-Attendance-System-using-OpenCV
This project helps to automate the door lock using face recognition . It is integrated with automatic attendance system using face recognition.

Technologies used: OpenCV, Python, Firebase, Arduino uno, Servo, Canva, Arduino ide.

Explaination of the working: 
Firstly we feed some faces (authorized faces) into our model, the door will recognize the authorized faces and open the door for 5 secs and automatically close the door. The project also marks the attendance for the day of the authorized users. In the attendance system we have 4 modes namely- Active mode, Information mode, Marked mode and Already marked mode. When no face is detected the application shows Active mode by default. When a known face is detected, the mode switches to information mode and then to marked mode. If the persons attendance is already marked the the mode changes to already marked mode.
