from PyQt5.QtWidgets import *
from urun_satis import Ui_Form
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
import mysql.connector

con = mysql.connector.connect(user='root',password = '',host = 'localhost',database = 'magazatakip')
cursor = con.cursor()


class Satis(QWidget):
    def __init__(self):
        super().__init__()
        self.satis = Ui_Form()
        self.satis.setupUi(self)
        self.satis.urunutani.clicked.connect(self.Tani)
        self.scene = QGraphicsScene(self)
        self.satis.goruntu.setScene(self.scene)
        self.webcam = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.is_camera_active = False
        self.net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=(320, 320), scale=1/255)
        self.satis.sat.clicked.connect(self.Sat)
        
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
            self.satis.goruntu.clearFocus()
            self.satis.goruntu.repaint()
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
                    self.satis.urunadi.setText(result[0])
                    self.current_class_name = class_name
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.scene.clear()
            self.scene.addPixmap(pixmap)
    
    def Sat(self):
        if hasattr(self, 'current_class_name'):
            class_name = self.current_class_name
            query = "SELECT adet FROM urunler WHERE urunadi = %s"
            cursor.execute(query, (class_name,))
            result = cursor.fetchone()
            if result:
                mevcut_adet = result[0]
                try:
                    adet = int(self.satis.urunadedi.text())
                except ValueError:
                    self.satis.urunadedi.setPlaceholderText('Geçerli bir sayı girin')
                    return
                if(adet>mevcut_adet):
                    QMessageBox.information(self,"Uyarı","Stok Yetersiz !")
                else:

                    yeni_adet = mevcut_adet - adet
                    query = "UPDATE urunler SET adet = %s WHERE urunadi = %s"
                    cursor.execute(query, (yeni_adet, class_name))
                    con.commit()
                    self.satis.urunadedi.clear()
                    self.satis.urunadi.clear()
                    QMessageBox.information(self,"Başarı","Satış Yapıldı !")
        else:
            self.satis.urunadi.setPlaceholderText('Ürün seçilmedi')

    def closeEvent(self, event):
        if self.is_camera_active and self.webcam.isOpened():
            self.webcam.release()
        super().closeEvent(event)
        
        

    



    

