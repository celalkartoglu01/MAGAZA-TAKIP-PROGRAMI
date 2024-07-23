from PyQt5.QtWidgets import *
from ana_sayfa import Ui_Form
from profil import Profil
from stokdurum import StokDurum
from calisanlar import Calisanlar
from satis import Satis
from iade import Iade

class AnaSayfa(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.anasayfa = Ui_Form()
        self.anasayfa.setupUi(self)
        self.profil = Profil()
        self.stokdurum = StokDurum()
        self.calisanlar = Calisanlar()
        self.satis = Satis()
        self.iade = Iade()
        self.anasayfa.profil.clicked.connect(self.Profil)
        self.anasayfa.stokdurum.clicked.connect(self.StokDurum)
        self.anasayfa.calisanlar.clicked.connect(self.Calisanlar)
        self.anasayfa.satis.clicked.connect(self.Satis)
        self.anasayfa.iade.clicked.connect(self.Iade)
        self.anasayfa.cikisyap.clicked.connect(self.CikisYap)
        
    


    def Profil(self):
        self.profil.show()
    

    def StokDurum(self):
        self.stokdurum.show()
    

    def Calisanlar(self):
        self.calisanlar.show()
    

    def Satis(self):
        self.satis.show()
    

    def Iade(self):
        self.iade.show()
    

    def CikisYap(self):
        self.hide()
        

    



    


       