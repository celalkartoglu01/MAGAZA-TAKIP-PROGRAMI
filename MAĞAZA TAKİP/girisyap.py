from PyQt5.QtWidgets import *
from giris_ import Ui_Form
from anasayfa import AnaSayfa
import mysql.connector



con = mysql.connector.connect(user='root',password = '',host = 'localhost',database = 'magazatakip')
cursor = con.cursor()



class Giris(QMainWindow):
    def __init__(self) ->  None:
        super().__init__()
        self.giris = Ui_Form()
        self.giris.setupUi(self)
        self.anasayfa = AnaSayfa()
        self.giris.girisyap.clicked.connect(self.GirisYap)
        self.giris.sifreyigoster.clicked.connect(self.SifreyiGoster)
    


    def GirisYap(self):
        kulladi = self.giris.kulladi.text()
        sifre = self.giris.sifre.text()

        kulladisorgu = "SELECT * FROM yonetici WHERE kulladi = %s"
        cursor.execute(kulladisorgu, (kulladi,))
        result_kullanici = cursor.fetchone()

        sifresorgu = "SELECT * FROM yonetici WHERE sifre = %s"
        cursor.execute(sifresorgu, (sifre,))
        result_sifre = cursor.fetchone()

        if result_kullanici and result_sifre:
            QMessageBox.information(self,"Başarı","Giriş Başarılı !")
            self.hide()
            self.anasayfa.show()
            self.giris.kulladi.clear()
            self.giris.sifre.clear()
        else:
            if not result_kullanici:
                QMessageBox.information(self,"Uyarı","Kullanıcı Adı Hatalı !")
            elif not result_sifre:
                QMessageBox.information(self,"Uyarı","Şifre Hatalı !")
            elif not result_kullanici and not result_sifre:
                QMessageBox.information(self,"Uyarı","Kullanıcı Adı ve Şifre Hatalı")

     
        

    
    def SifreyiGoster(self):
        current_echo_mode = self.giris.sifre.echoMode()
        if current_echo_mode == QLineEdit.Password:
            self.giris.sifre.setEchoMode(QLineEdit.Normal)
        else:
            self.giris.sifre.setEchoMode(QLineEdit.Password)
 
    
