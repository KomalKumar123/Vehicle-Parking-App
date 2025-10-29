# tasks/email_utils.py
import os
import smtplib
from email.message import EmailMessage
from typing import List, Tuple

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)

def send_email(to: str, subject: str, html_body: str, attachments: List[Tuple[str, bytes, str]] = None):
    """
    attachments: list of (filename, bytes_data, mime_type)
    mime_type example: 'text/csv' or 'application/pdf'
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to
    msg.set_content("This is an HTML email. If you see this, your client does not support HTML.")
    msg.add_alternative(html_body, subtype="html")

    if attachments:
        for filename, data, mime_type in attachments:
            maintype, subtype = mime_type.split("/", 1)
            msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    # send
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)
