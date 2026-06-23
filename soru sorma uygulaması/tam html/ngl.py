from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


GMAIL_ADRESIN = "----------------"  
UYGULAMA_SIFRESI = "fmfu pzmb mpqs atun" 

def mail_gonder(anonim_mesaj):
    try:
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_ADRESIN, UYGULAMA_SIFRESI)

        msg = MIMEMultipart()
        msg['From'] = GMAIL_ADRESIN
        msg['To'] = GMAIL_ADRESIN  
        msg['Subject'] = "Yeni Bir Anonim Soru Geldi!"

        body = f"Siteden yeni bir mesaj gönderildi:\n\n Mesaj: {anonim_mesaj}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        
        server.send_message(msg)
        server.quit()
        print("Mail başarıyla gönderildi!")
        return True
    except Exception as e:
        print(f"Mail gönderilirken hata oluştu: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/soru-gonder', methods=['POST'])
def soru_gonder():
    veri = request.json
    soru = veri.get('soru')
    
    if soru and soru.strip() != "":
      
        if mail_gonder(soru):
            return jsonify({"durum": "success", "mesaj": "Sorun başarıyla gönderildi!"}), 200
        else:
            return jsonify({"durum": "error", "mesaj": "Sistem hatası, mail gönderilemedi."}), 500
            
    return jsonify({"durum": "error", "mesaj": "Boş mesaj gönderemezsin!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)