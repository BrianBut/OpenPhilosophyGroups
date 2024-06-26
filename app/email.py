from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['LP_MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=app.config['LP_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    print("sender: {}".format(msg.sender))
    print("recipients: {}".format(msg.recipients))
    print("body: {}".format(msg.body))
    #mail.send(msg)