
from flask_login import UserMixin

from .extensions import db

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))




class DiyetSonucu(db.Model):
    __tablename__ = 'diyet_sonucu'
    id = db.Column(db.Integer, primary_key=True)
    cinsiyet = db.Column(db.String(10))
    yas = db.Column(db.Integer)
    kilo = db.Column(db.Float)
    boy = db.Column(db.Float)
    su = db.Column(db.Float)
    aktivite = db.Column(db.String(20))
    alerji = db.Column(db.String(20))
    uyku = db.Column(db.String(20))
    stres = db.Column(db.String(20))
    onerilen_diyet = db.Column(db.String(100))
    aciklama = db.Column(db.Text)
    bilgi_linki = db.Column(db.String(255)) 

    def __repr__(self):
        return f"<DiyetSonucu {self.id} - {self.onerilen_diyet}>"
   
