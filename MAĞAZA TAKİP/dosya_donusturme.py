from PyQt5 import uic

with open("giris_.py","w",encoding="utf-8") as fout:
    uic.compileUi("giris_yap.ui", fout)


with open("ana_sayfa.py","w",encoding="utf-8") as fout:
    uic.compileUi("ana_sayfa.ui", fout)



with open("calisanlar_.py","w",encoding="utf-8") as fout:
    uic.compileUi("calisanlar_.ui", fout)



with open("stok_durum.py","w",encoding="utf-8") as fout:
    uic.compileUi("stok_durum.ui", fout)



with open("urun_iade.py","w",encoding="utf-8") as fout:
    uic.compileUi("urun_iade.ui", fout)


with open("profil_.py","w",encoding="utf-8") as fout:
    uic.compileUi("profil_.ui", fout)


with open("urun_satis.py","w",encoding="utf-8") as fout:
    uic.compileUi("urun_satis.ui", fout)