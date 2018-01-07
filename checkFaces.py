import random
import time
from threading import Thread
import mysql.connector
import face_recognition
import cv2
 
students = []
studentsID = []
lastTime = time.time()-60000
class MySQLThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.name = 'takeInfoThread'
        self.db_host = 'localhost'
        self.db_user = 'usr'
        self.db_password = 'pass'
        self.db_name = 'students'
        self.connection = mysql.connector.connect(user=self.db_user, password=self.db_password,host=self.db_host,database=self.db_name)
        self.query = ("SELECT * FROM students")

    def run(self):
        if time.time()-lastTime>=60000:
            lastTime = time.time()
            self.cursor = connection.cursor()
            cursor.execute(query)
            students = []
            for (name, surname, middle_name, class_num, class_let, phone, face_recog) in cursor:
                students.append((name,surname,middle_name,class_num,class_let,phone,face_recog))
            studentsID = []
            for person in students:
                studentsID.append(person[6])

def create_threads():
    SQLthread=MySQLThread()
    SQLthread.start()



if __name__ == "__main__":
    create_threads()
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "???"
            for i in range(len(studentsID)):
                ID = studentsID[i]
                match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
                if match[0]:
                    name = students[i][0]+" "+students[i][1]+" "+students[i][2]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

