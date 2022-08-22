import smtplib

from email.message import EmailMessage

msg = EmailMessage()

conection = smtplib.SMTP_SSL('smtp.gmail.com', 456)
conection.login('phgedi48@gmail.com', "bfvgemhgmosywrwn")
conection.sendmail(
    from_addr="",
    to_addrs="",
    msg=""
    )