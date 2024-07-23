from PyQt5.QtWidgets import *
from stok_durum import Ui_Form
import mysql.connector




con = mysql.connector.connect(user='root', password='', host='localhost', database='magazatakip')
cursor = con.cursor()


class StokDurum(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.stokdurum = Ui_Form()
        self.stokdurum.setupUi(self)
        self.stokdurum.kategoriler.currentIndexChanged.connect(self.kategori_degisti)
    

    def kategori_degisti(self):
        secili_kategori = self.stokdurum.kategoriler.currentText()

        cursor.execute("SELECT * FROM urunler WHERE kategori=%s", (secili_kategori,))
        urunler = cursor.fetchall()

        toplam_adet = 0
        column_names = [i[0] for i in cursor.description]
        for row in urunler:
            adet_index = column_names.index('adet')
            toplam_adet += row[adet_index]

        self.stokdurum.urunadedi.setText(str(toplam_adet))
        
        column_names = [i[0] for i in cursor.description]

        self.stokdurum.urunler.setColumnCount(len(column_names))
        self.stokdurum.urunler.setHorizontalHeaderLabels(column_names)

        self.stokdurum.urunler.setRowCount(len(urunler))

        for row_index, row_data in enumerate(urunler):
            for column_index, data in enumerate(row_data):
                self.stokdurum.urunler.setItem(row_index, column_index, QTableWidgetItem(str(data)))

        self.stokdurum.urunler.resizeColumnsToContents()

        table_width = self.stokdurum.urunler.width()

        total_width = sum(self.stokdurum.urunler.columnWidth(i) for i in range(len(column_names)))
        for i in range(len(column_names)):
            self.stokdurum.urunler.setColumnWidth(i, int(self.stokdurum.urunler.columnWidth(i) * table_width / total_width))

        self.stokdurum.urunler.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        

    



    

