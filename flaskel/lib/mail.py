#-*- coding: utf-8 -*-

"""
    flaskel/lib/mail.py
    -------------------

    Composes an email and sends it to a recipient specified.
"""

from contextlib import contextmanager
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate

from jinja2 import Environment, PackageLoader

from flaskel import app


def get_template(template_name):
    """Load an email template."""
    return Environment(loader=PackageLoader("flaskel")).get_template(
        template_name
    )


@contextmanager
def _get_smtp_conn(server, port, user, password):
    conn = smtplib.SMTP(server, port)
    try:
        conn.login(user, password)
        yield conn
    finally:
        conn.close()


def send(recipient, subject, message, sender):
    """Send an email via SMTP."""
    if app.config["DEBUG"]:
        return False

    msg = MIMEMultipart()
    msg["from"] = sender
    msg["To"] = recipient
    msg["date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain", "UTF-8"))

    with _get_smtp_conn(server=app.config["EMAIL"]["SERVER"],
                        port=app.config["EMAIL"]["PORT"],
                        user=app.config["EMAIL"]["USER"],
                        password=app.config["EMAIL"]["PASSWORD"]) as conn:
        conn.sendmail(sender, recipient, msg.as_string())
        return True

    return False
