from PyQt5.QtWidgets import *
from profil_ import Ui_Form
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
import face_recognition
import os
import numpy as np
import mysql.connector

con = mysql.connector.connect(user='root', password='', host='localhost', database='magazatakip')
cursor = con.cursor()


class Profil(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.profil = Ui_Form()
        self.profil.setupUi(self)
        self.profil.dogrula.clicked.connect(self.Dogrula)
        self.scene = QGraphicsScene(self)
        self.profil.goruntu.setScene(self.scene)
        self.webcam = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.known_face_encodings = []
        self.known_face_names = []
        self.folder_path = "yoneticiler"
        self.is_camera_active = False
        self.update_known_faces()
    

    def update_known_faces(self):
        self.known_face_encodings = []
        self.known_face_names = []
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png"):
                image_path = os.path.join(self.folder_path, file_name)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)[0]
                self.known_face_encodings.append(encoding)
                self.known_face_names.append(os.path.splitext(file_name)[0])
    

    def Dogrula(self):
        if self.is_camera_active:
            self.webcam.release()
            self.timer.stop()
            self.scene.clear() 
            self.profil.goruntu.clearFocus() 
            self.profil.goruntu.repaint() 
            self.is_camera_active = False
        else:
            self.webcam = cv2.VideoCapture(0)
            self.timer.start(20)
            self.is_camera_active = True
    

    def updateFrame(self):
        ret, frame = self.webcam.read()

        if ret:
            frame = cv2.flip(frame,1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame,face_locations)

            for face_encoding, (topLeftY, botRightX, botRightY, topLeftX) in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Bilinmeyen Yuz"
                if any(matches):
                    matched_index = np.argmax(matches)
                    name = self.known_face_names[matched_index]
                    query = "select ad,soyad,unvan from yonetici where kulladi = %s"
                    cursor.execute(query,(name,))
                    result = cursor.fetchone()
                    ad,soyad,unvan = result
                    self.profil.ad.setText(ad)
                    self.profil.soyad.setText(soyad)
                    self.profil.unvan.setText(unvan)
                else:
                    cv2.rectangle(frame, (topLeftX, topLeftY), (botRightX, botRightY), (0,0,255), 2)
                    cv2.putText(frame, name, (topLeftX, topLeftY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        
        qImg = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qImg)
        self.scene.clear()
        self.scene.addPixmap(pixmap)


        
        

    



    

