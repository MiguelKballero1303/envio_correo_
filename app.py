import logging
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

EMAIL_SENDER = "miguel.lynch130304@gmail.com"
EMAIL_PASSWORD = "ityt logd wefn uhlq"
EMAIL_RECEIVER = "miguel.lynch130304@gmail.com"

def enviar_correo(name, email, subject, message):
    try:
        # 🔹 Crear el mensaje con formato HTML
        msg = MIMEMultipart()
        msg["Subject"] = f"📩 Nuevo Mensaje de {name} - {subject}"
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        # 🔹 Contenido del correo en HTML
        contenido_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #007BFF;">📬 Nuevo Mensaje Recibido</h2>
            <p><strong>📌 Nombre:</strong> {name}</p>
            <p><strong>📧 Correo:</strong> {email}</p>
            <p><strong>📖 Asunto:</strong> {subject}</p>
            <hr>
            <p style="font-size: 14px;"><strong>✉️ Mensaje:</strong></p>
            <p style="border-left: 3px solid #007BFF; padding-left: 10px;">{message}</p>
            <hr>
            <p style="font-size: 12px; color: #888;">Este mensaje fue enviado a través del formulario de contacto.</p>
        </body>
        </html>
        """

        # 🔹 Adjuntar el contenido HTML
        msg.attach(MIMEText(contenido_html, "html"))

        # 🔹 Configurar servidor SMTP y enviar correo
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        logging.info("✅ Correo enviado con éxito")
        return True
    except Exception as e:
        logging.error(f"❌ Error al enviar el correo: {e}")
        return False

@app.route('/enviar_correo', methods=['POST'])
def recibir_formulario():
    try:
        data = request.json
        logging.info(f"📩 Datos recibidos: {data}")

        if not data:
            return jsonify({"status": "error", "message": "No se recibieron datos"}), 400

        name = data.get("name")
        email = data.get("email")
        subject = data.get("subject")
        message = data.get("message")

        if not all([name, email, subject, message]):
            logging.warning("⚠️ Faltan datos en la solicitud")
            return jsonify({"status": "error", "message": "Todos los campos son obligatorios"}), 400

        if enviar_correo(name, email, subject, message):
            return jsonify({"status": "success", "message": "Correo enviado con éxito"})
        else:
            return jsonify({"status": "error", "message": "No se pudo enviar el correo"}), 500
    except Exception as e:
        logging.error(f"❌ Error en la solicitud: {e}")
        return jsonify({"status": "error", "message": "Error en el servidor"}), 500

if __name__ == '__main__':
    app.run(debug=True)
