# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content("apenas um teste")

# me == the sender's email address
# you == the recipient's email address
msg['Subject'] = "Isso é um teste"
msg['From'] = "phgedi48@gmail.com"
msg['To'] = "pedro.dicati@estudante.ifms.edu.br"

# Send the message via our own SMTP server.

conection = smtplib.SMTP('smtp.gmail.com', port = 456)
conection.login('phgedi48@gmail.com', "bfvgemhgmosywrwn")
conection.send_message(msg)
conection.quit()
