from __future__ import print_function
import smtplib
from email.mime.text import MIMEText


class GMailer:
    """
    Send emails using Gmail.
    """
    def __init__(self, username, password, host, port, gmail=True):
        if type(username) != str and type(username) != unicode:
            raise TypeError('A string was expected for the username variable.')
        if type(password) != str and type(password) != unicode:
            raise TypeError('A string was expected for the password variable.')
        if type(host) != str and type(host) != unicode:
            raise TypeError('A string was expected for the host variable.')
        if type(port) != int:
            try:
                port = int(port)
            except ValueError:
                raise TypeError('An integer was expected for the port variable.')

        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.gmail = gmail

    def send_email(self, emails, subject, the_msg):
        """
        Send an email.

        :param emails:
        :param subject:
        :param the_msg:
        :return:
        """

        email_list = emails.split(',')
        email_list = [email.strip() for email in email_list]

        msg = "\r\n".join([
            "From: {}".format(self.username),
            "To: {}".format(emails),
            "Subject: {}".format(subject)
        ])

        msg += "\r\n{}".format(the_msg)
        smtp = smtplib.SMTP("{}:{}".format(self.host, self.port))
        print("Sending report...")
        if self.gmail:
            print(smtp.ehlo())
            print(smtp.starttls())
        print(smtp.login(self.username, self.password))
        print()
        print(smtp.sendmail(self.username, email_list, msg))
        smtp.close()
        return self

    def send_email_with_attachment(self, emails, filepath, subject):
        """
        Send an email with an attachment.

        :param emails:
        :param filepath:
        :param subject:
        :return:
        """

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
        if self.gmail:
            print(smtp.ehlo())
            print(smtp.starttls())
        print(smtp.login(self.username, self.password))
        print()
        print(smtp.sendmail(self.username, email_list, msg))
        smtp.close()
        return self
