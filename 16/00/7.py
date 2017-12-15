import ssl, smtplib
smtp = smtplib.SMTP("mail.python.org", port=587)
context = ssl.create_default_context()
print(smtp.starttls(context=context))
