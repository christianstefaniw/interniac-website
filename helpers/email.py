import threading

from django.core.mail import EmailMessage


def send_email_thread(from_email, body, to, subject, reply_to) -> None:
    def _send():
        EmailMessage(body=body, from_email=from_email,
                     to=to, subject=subject,
                     reply_to=reply_to).send()

    x = threading.Thread(target=_send)
    x.start()


def send_email(from_email, body, to, subject, reply_to) -> None:
    EmailMessage(body=body, from_email=from_email,
                 to=to, subject=subject,
                 reply_to=reply_to).send()
