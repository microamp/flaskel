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

from flaskel import config as cfg


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
    if getattr(cfg, "DEBUG", False):
        return False

    msg = MIMEMultipart()
    msg["from"] = sender
    msg["To"] = recipient
    msg["date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain", "UTF-8"))

    with _get_smtp_conn(server=cfg.EMAIL["SERVER"],
                        port=cfg.EMAIL["PORT"],
                        user=cfg.EMAIL["USER"],
                        password=cfg.EMAIL["PASSWORD"]) as conn:
        conn.sendmail(sender, recipient, msg.as_string())
        return True

    return False
