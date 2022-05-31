from threading import Thread
from email.message import EmailMessage
import email.utils
from flask import render_template
from app import app, smtp


def send_email(subject, sender, recipients, text_body, html_body):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = ','.join(recipients)
    msg['Subject'] = subject
    msg['Date'] = email.utils.localtime()
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')
    Thread(target=smtp.send_message, args=(msg, sender, recipients)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Blog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))
