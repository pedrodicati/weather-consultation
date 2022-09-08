import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_login = "phgedi48@gmail.com"
password = 'bfvgemhgmosywrwn'

to = "pedro.dicati@estudante.ifms.edu.br"

smtp_server = 'smtp.gmail.com'
smtp_port = 587

message = MIMEMultipart('alternative')

message['Subject'] = "Só um teste"
message['From'] = email_login
message['To'] = to

text = "Esse é o texto que vai no email"

message_text = MIMEText(text, 'plain')

message.attach(message_text)

mail = smtplib.SMTP(smtp_server, smtp_port)

print(mail)

mail.ehlo()

mail.starttls()

mail.login(email_login, password)

mail.sendmail(email_login, to, message.as_string())
mail.quit()
