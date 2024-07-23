from PyQt5.QtWidgets import *
from calisanlar_ import Ui_Form
import mysql.connector



con = mysql.connector.connect(user='root',password = '',host = 'localhost',database = 'magazatakip')
cursor = con.cursor()



class Calisanlar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.calisanlar = Ui_Form()
        self.calisanlar.setupUi(self)
        self.calisanlar.getir.clicked.connect(self.Getir)
    


    def Getir(self):
        query = "select ad,soyad,unvan from calisanlar"
        cursor.execute(query)
        veriler = cursor.fetchall()
        self.calisanlar.calisanlar.setRowCount(len(veriler))
        self.calisanlar.calisanlar.setColumnCount(3)
        self.calisanlar.calisanlar.setHorizontalHeaderLabels(["Ad", "Soyad","Unvan"])
        for satir,kayit in enumerate(veriler):
            for sutun, deger in enumerate(kayit):
               self.calisanlar.calisanlar.setItem(satir,sutun,QTableWidgetItem(str(deger)))
        self.calisanlar.calisanlar.resizeColumnsToContents()

        table_width = self.calisanlar.calisanlar.width()

        total_width = sum(self.calisanlar.calisanlar.columnWidth(i) for i in range(3))
        for i in range(3):
            self.calisanlar.calisanlar.setColumnWidth(i, int(self.calisanlar.calisanlar.columnWidth(i) * table_width / total_width))

        self.calisanlar.calisanlar.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.calisanlar.calisanadedi.setText(str(len(veriler)))
        

    



    

