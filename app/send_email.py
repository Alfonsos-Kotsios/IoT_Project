import smtplib
from email.message import EmailMessage
import time

# Cooldown ανά τύπο alert (σε δευτερόλεπτα)
COOLDOWN_SECONDS = 300  # 10 λεπτά

# Καταγραφή τελευταίων αποστολών
last_alert_times = {
    "light": 0,
    "temperature": 0,
    "humidity": 0
}
EMAIL_ADDRESS = "alfonsostrela@gmail.com"
EMAIL_PASSWORD = "zivv imso gqag hsip"  # Use App Password if using Gmail 2FA


user_settings = {
    "email": "alfonsos.l23@hotmail.com",
    "LIGHT_THRESHOLD": 500,
    "TEMP_THRESHOLD": 30,
    "HUMIDITY_THRESHOLD": 70,
    "LIGHT_LOW_THRESHOLD": 100,
    "TEMP_LOW_THRESHOLD": 10,
    "HUMIDITY_LOW_THRESHOLD": 30,
    "COOLDOWN_SECONDS": 600
}


def send_alert_email(subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_settings["email"]
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
