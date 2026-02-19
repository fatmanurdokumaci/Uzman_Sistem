from flask import Flask,request,jsonify,session,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .extensions import db

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'TEXT'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'TEXT'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) 
    
    
    with app.app_context():
        from .models import DiyetSonucu, User  
        db.create_all()
   
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

   
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    def vki_hesapla(kilo, boy):
        return kilo / ((boy / 100) ** 2)

    def diyet_oner(cevaplar):
        kilo = float(cevaplar["kilo"])
        boy = float(cevaplar["boy"])
        su = float(cevaplar["su"])
        aktivite = cevaplar["aktivite"]
        alerji = cevaplar["alerji"]
        uyku = cevaplar["uyku"]
        stres = cevaplar["stres"]
        cinsiyet = cevaplar.get("cinsiyet", "Belirtilmemiş")
        yas = int(cevaplar["yas"])

        def vki_hesapla(kilo, boy):
            return kilo / ((boy / 100) ** 2)

        vki = vki_hesapla(kilo, boy)

        
        if vki < 18.5:
            kilo_durumu = "Zayıf"
        elif 18.5 <= vki < 25:
            kilo_durumu = "Sağlıklı"
        elif 25 <= vki < 30:
            kilo_durumu = "Fazla kilolu"
        elif 30 <= vki < 40:
            kilo_durumu = "Obez"
        else:
            kilo_durumu = "Aşırı Obez (Morbid Obez)"

       
        temel_su_ihtiyaci = kilo * 0.03
        if cinsiyet == "Erkek":
            temel_su_ihtiyaci += 0.5
        elif cinsiyet == "Kadın":
            temel_su_ihtiyaci += 0.25
        if yas >= 55:
            temel_su_ihtiyaci -= 0.25

        
        aciklama = f" Vücut Kitle İndeksiniz: {vki:.1f}, kilo durumunuz: {kilo_durumu}. "

    
        if su < temel_su_ihtiyaci:
            aciklama += f"Günlük su ihtiyacınız yaklaşık {temel_su_ihtiyaci:.1f} litredir. Mevcut su tüketiminiz bu miktarın altında, lütfen su alımınızı artırınız. "

     
        if aktivite == "Düşük":
            aciklama += "Fiziksel aktivite seviyeniz düşük. Haftada en az 30 dakika orta şiddette egzersiz önerilir. "
        elif aktivite == "Orta":
            aciklama += "Orta düzeyde fiziksel aktivite yapıyorsunuz. Egzersiz sıklığınızı artırmak sağlığınız için faydalı olacaktır. "

        
        if uyku == "Düzensiz":
            aciklama += "Uyku düzeniniz sağlığınızı etkiliyor. Günde 7-9 saat düzenli uyku önemlidir. "

     
        if stres == "Yüksek":
            aciklama += "Stres seviyeniz yüksek, bu durum bağışıklık ve sindirim sisteminizi olumsuz etkileyebilir. "

     

        if vki > 30:
            if aktivite == "Düşük" and uyku == "Düzensiz" and su < temel_su_ihtiyaci:
                return {
                    "diyet": "Şok Diyet",
                    "aciklama": aciklama + "Vücut kitle indeksiniz obez sınıfında, düşük aktivite, düzensiz uyku ve yetersiz su tüketimi hızlı kilo kaybı gerektiriyor. Kısa sürede etkili olan Şok Diyet önerilir. Uzun vadede önerilmez.",
                    "bilgi_linki": "https://www.pinardemirkaya.com.tr/diyetler/sok-diyet/"
                }
            elif stres == "Yüksek":
                return {
                    "diyet": "Akdeniz Diyeti",
                    "aciklama": aciklama + "Yüksek stres seviyeniz nedeniyle inflamasyonu azaltan Akdeniz Diyeti önerilmektedir.",
                    "bilgi_linki": "https://unimeal.com/tr/lp20?utm_source=google_search&utm_medium=153804868239&utm_campaign=20550460041"
                }
            elif alerji == "Gluten":
                return {
                    "diyet": "Glutensiz Diyet",
                    "aciklama": aciklama + "Gluten intoleransınız var. Glutensiz diyet sağlık için gereklidir.",
                    "bilgi_linki": "https://www.memorial.com.tr/saglik-rehberi/glutensiz-diyet-nedir"
                }
            elif aktivite == "Düşük" and uyku == "Düzensiz":
                return {
                    "diyet": "Düşük Karbonhidrat Diyeti",
                    "aciklama": aciklama + "Düşük aktivite ve düzensiz uyku nedeniyle karbonhidrat azaltımı önerilir.",
                    "bilgi_linki": "https://www.pinardemirkaya.com.tr/diyetler/dusuk-karbonhidrat-diyeti/"
                }
            else:
                return {
                    "diyet": "Ketojenik Diyet",
                    "aciklama": aciklama + "Obezite durumunda düşük karbonhidrat ve yüksek yağ içeren Ketojenik Diyet önerilmektedir.",
                    "bilgi_linki": "https://www.memorial.com.tr/saglik-rehberi/ketojenik-diyet-nedir-nasil-yapilir"
                }

        elif 25 < vki <= 30:
            if aktivite in ["Orta", "Yüksek"] and alerji != "Protein":
                return {
                    "diyet": "Dukan Diyeti",
                    "aciklama": aciklama + "Fazla kilolu ve yeterli aktivite seviyeniz ile Dukan Diyeti önerilmektedir.",
                    "bilgi_linki": "https://www.pinardemirkaya.com.tr/diyetler/dukan-diyeti/"
                }
            elif aktivite == "Orta":
                return {
                    "diyet": "Dengeli Diyet",
                    "aciklama": aciklama + "Kontrollü kalori alımı ile Dengeli Diyet önerilir.",
                    "bilgi_linki": "https://www.alifesaglikgrubu.com.tr/makale/diyet-listesi/3740"
                }
            elif uyku == "Düzenli":
                return {
                    "diyet": "Akdeniz Diyeti",
                    "aciklama": aciklama + "Düzenli uyku metabolizmanızı destekliyor, Akdeniz Diyeti önerilir.",
                    "bilgi_linki": "https://aysetugbasengel.com/akdeniz-diyeti-nedir-diyet-listesi-ornegi/"
                }
            elif alerji == "Laktoz":
                return {
                    "diyet": "Laktozsuz Diyet",
                    "aciklama": aciklama + "Laktoz intoleransınız için Laktozsuz Diyet uygundur.",
                    "bilgi_linki": "https://diyetisyengamzealtinay.com/2023/12/13/laktozsuz-beslenme-nedir-laktoz-intoleransi-beslenme-onerileri/"
                }
            else:
                return {
                    "diyet": "Vejetaryen Diyet",
                    "aciklama": aciklama + "Bitkisel temelli Vejetaryen Diyet önerilmektedir.",
                    "bilgi_linki": "https://aysetugbasengel.com/vegan-beslenme-nedir-vegan-diyeti-nasil-yapilir/"
                }

        elif 18.5 <= vki <= 25:
            if aktivite == "Yüksek":
                return {
                    "diyet": "Yüksek Proteinli Diyet",
                    "aciklama": aciklama + "Yüksek aktivitenizle kas yapınızı koruyacak Yüksek Proteinli Diyet önerilir.",
                    "bilgi_linki": "https://www.acibadem.com.tr/hayat/yuksek-protein-diyeti-nedir/"
                }
            elif uyku == "Düzensiz" and stres == "Yüksek":
                return {
                    "diyet": "Anti-inflamatuar Diyet",
                    "aciklama": aciklama + "Uyku bozukluğu ve yüksek stres nedeniyle Anti-inflamatuar Diyet önerilir.",
                    "bilgi_linki": "https://www.birunihastanesi.com.tr/saglik-rehberi/anti-inflamatuar-diyet-nedir"
                }
            elif uyku == "Düzensiz":
                return {
                    "diyet": "Dengeli Diyet",
                    "aciklama": aciklama + "Uyku düzensizliğine karşı Dengeli Diyet önerilmektedir.",
                    "bilgi_linki": "https://www.alifesaglikgrubu.com.tr/makale/diyet-listesi/3740"
                }
            elif stres == "Yüksek":
                return {
                    "diyet": "MIND Diyeti",
                    "aciklama": aciklama + "Yüksek stres nedeniyle beyin sağlığını destekleyen MIND Diyeti önerilir.",
                    "bilgi_linki": "https://bilimgenc.tubitak.gov.tr/makale/mind-diyeti-saglikli-bir-beyin-icin-nasil-beslenmeli"
                }
            else:
                return {
                    "diyet": "Zon Diyeti",
                    "aciklama": aciklama + "Genel sağlık durumunuzu korumak için Zon Diyeti uygundur.",
                    "bilgi_linki": "https://aysetugbasengel.com/zone-diyeti-nedir-kilo-verdirir-mi/"
                }

        elif vki < 18.5:
            if stres == "Yüksek":
                return {
                    "diyet": "Yüksek Kalorili Dengeli Diyet",
                    "aciklama": aciklama + "Zayıfsınız ve stresiniz yüksek. Sağlıklı kilo alımı için önerilir.",
                    "bilgi_linki": "https://www.nefisyemektarifleri.com/blog/kilo-alma-programi-kilo-aldiran-diyet-listesi/"
                }
            else:
                return {
                    "diyet": "Besleyici Yoğun Diyet",
                    "aciklama": aciklama + "Zayıf kategorisindesiniz, besleyici yoğun diyet önerilir.",
                    "bilgi_linki": "https://gozdesahin.com/kilo-aldirici-ornek-liste"
                }

       
        return {
            "diyet": "Dengeli Diyet",
            "aciklama": aciklama + "Genel sağlığınızı destekleyecek dengeli bir diyettir.",
            "bilgi_linki": "https://www.alifesaglikgrubu.com.tr/makale/diyet-listesi/3740"
        }


    @app.route("/")
    def index():
        session.clear()
        return render_template("index.html")

    @app.route("/submit", methods=["POST"])
    def submit():
        data = request.get_json()
        for key, value in data.items():
            session[key] = value
        return jsonify({"status": "ok"})

    @app.route("/result")
    def result():
        cevaplar = dict(session)
        sonuc = diyet_oner(cevaplar)

        yeni_kayit = DiyetSonucu(
            cinsiyet=cevaplar.get("cinsiyet"),
            yas=int(cevaplar.get("yas")),
            kilo=float(cevaplar.get("kilo")),
            boy=float(cevaplar.get("boy")),
            su=float(cevaplar.get("su")),
            aktivite=cevaplar.get("aktivite"),
            alerji=cevaplar.get("alerji"),
            uyku=cevaplar.get("uyku"),
            stres=cevaplar.get("stres"),
            onerilen_diyet=sonuc["diyet"],
            aciklama=sonuc["aciklama"],
            bilgi_linki=sonuc["bilgi_linki"]
        )
        print("basarıli")
        db.session.add(yeni_kayit)
        db.session.commit()

        return jsonify(sonuc)


    

    return app
