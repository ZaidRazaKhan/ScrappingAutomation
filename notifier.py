import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""

class Notifier:
    def __init__(self, sender, receiver, password):
        self.sender_email = sender
        self.receiver_email = receiver
        self.password = password

    def notify(self, text, subject):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        part = MIMEText(text, "plain")
        message.attach(part)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.receiver_email, message.as_string()
            )

