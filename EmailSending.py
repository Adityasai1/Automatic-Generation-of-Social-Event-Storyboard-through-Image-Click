import smtplib
class EmailSending:
    
    def send_email(self, subject, msg, to):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login("myprojectcheck9@gmail.com","Project@12345")
            message = 'Subject: {}\n\n{}'.format(subject, msg)
            server.sendmail(to, to, message)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")
