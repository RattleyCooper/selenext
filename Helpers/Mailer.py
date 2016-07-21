import smtplib
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def send_email(self, emails, subject, the_msg):
        email_list = emails.split(',')
        email_list = [email.strip() for email in email_list]

        msg = "\r\n".join([
            "From: {}".format(self.username),
            "To: {}".format(emails),
            "Subject: {}".format(subject)
        ])

        msg += "\r\n{}".format(the_msg)
        smtp = smtplib.SMTP("{}:{}".format(self.host, self.port))
        print "Sending report..."
        print smtp.ehlo()
        print smtp.starttls()
        print smtp.login(self.username, self.password)
        print
        print smtp.sendmail(self.username, email_list, msg)
        smtp.close()

    def send_email_with_attachment(self, emails, filepath, subject):
        email_list = emails.split(',')
        email_list = [email.strip() for email in email_list]

        msg = "\r\n".join([
            "From: {}".format(self.username),
            "To: {}".format(emails),
            "Subject: {}".format(subject)
        ])

        with open(filepath, 'rb') as f:
            attachment = MIMEText(f.read())

        attachment.add_header('Content-Disposition', 'attachment', filename=filepath)

        msg += "\r\n" + attachment.as_string()

        smtp = smtplib.SMTP("{}:{}".format(self.host, self.port))
        print smtp.ehlo()
        print smtp.starttls()
        print smtp.login(self.username, self.password)
        print
        print smtp.sendmail(self.username, email_list, msg)
        smtp.close()