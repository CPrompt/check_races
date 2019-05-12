#!/usr/bin/python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import loginfo.creds as Secrets
import read_json
import update_json


# email vars
fromEmail = Secrets.login['fromEmail']
toEmail = Secrets.login['toEmail']
emailLogin = Secrets.login['emailLogin']
emailPass = Secrets.login['emailPass']
emailServer = Secrets.login['emailServer']
emailPort = Secrets.login['emailPort']


'''
    function to send SMS via email
'''
def send_email(emailSubject,emailBody):
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = toEmail
    msg['Subject'] = emailSubject

    body = emailBody

    msg.attach(MIMEText(body,'plain'))

    s = smtplib.SMTP(emailServer,emailPort)
    s.ehlo()
    s.starttls()
    s.login(emailLogin,emailPass)
    text = msg.as_string()
    s.sendmail(fromEmail,toEmail,text)
    s.quit()


if __name__ == "__main__":
    if read_json.output_config()["motogp_rtorrent_email"] == "No":
        motogp_partition = read_json.output_config()["motogp_title"].partition(":")
        send_email("New MotoGP Race ready to watch",motogp_partition[0])
        update_json.updateJsonFile("motogp_rtorrent_email","Yes")

    if read_json.output_config()["formula1_rtorrent_email"] == "No":
        motogp_partition = read_json.output_config()["formula1_title"].partition(":")
        send_email("New Formula1 Race ready to watch",motogp_partition[0])
        update_json.updateJsonFile("formula1_rtorrent_email","Yes")
