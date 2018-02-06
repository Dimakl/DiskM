import face_recognition
import pymysql.cursors
import cv2
import threading
import json
import time
import numpy

video_capture = cv2.VideoCapture(0)
students_encodings = []
students_data = []

HOST = 'localhost'
USER = 'root'
DB = 'data'
CHARSET = 'utf8mb4'
def get_data():
    while True:
        connection = pymysql.connect(host=HOST,
                                     user=USER,
                                     password='xyzzy',
                                     db=DB,
                                     charset=CHARSET,
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `students`"
                cursor.execute(sql)
                change_students_data = []
                change_students_encodings = []
                result = cursor.fetchone()
                while result is not None:
                    print(result)
                    change_students_data.append([result['name'],result['surname'],result['middle_name'],result['class_let'],result['phone']])
                    change_students_encodings.append(numpy.asarray(json.loads(result['face_enc'])))
                    result = cursor.fetchone()
                global students_data
                global students_encodings
                students_data = change_students_data
                students_encodings = change_students_encodings
                print(students_data)
                print(change_students_data)
        finally:
            connection.close()
            time.sleep(60)

t = threading.Thread(target=get_data)
t.start()
face_locations = []
face_encodings = [] #TODO: parse endcodings from MySQL DB
face_names = [] #TODO:change to data about students
process_this_frame = True
while True:
    ret, frame = video_capture.read()
    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    rgb_small_frame = small_frame[:, :, ::-1]
    
    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(students_encodings, face_encoding)
            person_data = ['???','???','???','?','Unknown']
            if True in matches:
                first_match_index = matches.index(True)
                person_data = students_data[first_match_index]
            
            face_names.append(person_data)

    process_this_frame = not process_this_frame
    
    
    for (top, right, bottom, left), data in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        outp_text = data[1]
        text_size = 1.0
        if (len(outp_text) > 10):
            text_size = 0.8
        if (len(outp_text) > 20):
            text_size = 0.6
        cv2.putText(frame, outp_text, (left + 6, bottom - 6), font, text_size, (255, 255, 255), 1)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

t._stop() #TODO: fix the stop of the thread
video_capture.release()
cv2.destroyAllWindows()

