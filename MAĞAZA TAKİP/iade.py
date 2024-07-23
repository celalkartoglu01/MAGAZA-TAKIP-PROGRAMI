from PyQt5.QtWidgets import *
from urun_iade import Ui_Form
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import mysql.connector

con = mysql.connector.connect(user='root',password = '',host = 'localhost',database = 'magazatakip')
cursor = con.cursor()

class Iade(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.iade = Ui_Form()
        self.iade.setupUi(self)
        self.iade.urunutani.clicked.connect(self.Tani)
        self.scene = QGraphicsScene(self)
        self.iade.goruntu.setScene(self.scene)
        self.webcam = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_active = False
        self.net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(320, 320), scale=1/255)
        self.iade.iadeal.clicked.connect(self.IadeAl)
        
        self.classes = []
        with open("dnn_model/classes.txt", "r",encoding="utf-8") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()  
                self.classes.append(class_name)

    def Tani(self):
        if self.is_camera_active:
            self.webcam.release()
            self.timer.stop()
            self.scene.clear()
            self.iade.goruntu.clearFocus()
            self.iade.goruntu.repaint()
            self.is_camera_active = False
        else:
            self.webcam = cv2.VideoCapture(0)
            if not self.webcam.isOpened():
                print("Webcam açılamadı!")
                return
            self.timer.start(20)
            self.is_camera_active = True

    def update_frame(self):
        ret, frame = self.webcam.read()
        if ret:
            frame = cv2.flip(frame, 1)
            (class_ids, scores, bboxes) = self.model.detect(frame, confThreshold=0.3, nmsThreshold=0.4)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                (x, y, w, h) = bbox
                cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 50), 3)
                class_name = self.classes[class_id]

                cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200, 0, 50), 2)

                query = "select urunadi from urunler where urunadi = %s"
                cursor.execute(query,(class_name,))
                result = cursor.fetchone()
                if result:
                    self.iade.urunadi.setText(result[0])
                    self.current_class_name = class_name
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
    
    def IadeAl(self):
        if hasattr(self, 'current_class_name'):
            class_name = self.current_class_name
            query = "SELECT adet FROM urunler WHERE urunadi = %s"
            cursor.execute(query, (class_name,))
            result = cursor.fetchone()
            if result:
                mevcut_adet = result[0]
                try:
                    adet = int(self.iade.urunadedi.text())
                except ValueError:
                    self.iade.urunadedi.setPlaceholderText('Geçerli bir sayı girin')
                    return
                yeni_adet = mevcut_adet + adet
                query = "UPDATE urunler SET adet = %s WHERE urunadi = %s"
                cursor.execute(query, (yeni_adet, class_name))
                con.commit()
                iadenedeni = self.iade.iadenedeni.text()
                query = "insert into iade (urunadi,adet,iadenedeni) values(%s,%s,%s)"
                cursor.execute(query,(self.current_class_name,adet,iadenedeni))
                con.commit()

                self.iade.urunadedi.clear()
                self.iade.urunadi.clear()
                self.iade.iadenedeni.clear()
                QMessageBox.information(self,"Başarı","İade Alındı !") 
        else:
            self.iade.urunadi.setPlaceholderText('Ürün seçilmedi')

    def closeEvent(self, event):
        if self.is_camera_active and self.webcam.isOpened():
            self.webcam.release()
        super().closeEvent(event)
        

    



    

