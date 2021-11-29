from django.core.mail import send_mail
from celery import shared_task
import jwt
import os


def encode(user_id):
    return jwt.encode({"userId": user_id}, os.getenv("JWT_SECRET"), algorithm="HS256")


def token_decode(token):
    return jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])


@shared_task
def send_reset_password_mail(user_id, user_email, callback_url):
    token = encode(user_id)

    HTML_MESSAGE = f"""
        <p>Please click the url to reset your password</p>
        <h4><a href="{callback_url}/?token={token}">Reset my password</a></h4>.
        <p>If it\'s inside your spam box please mark it as not spam first, otherwise the link might not be visible</p>
    """

    send_mail(
        "Reset Password | Strativ News Portal",
        "",
        html_message=HTML_MESSAGE,
        from_email=os.getenv("SEND_FROM_EMAIL"),
        recipient_list=[user_email],
        fail_silently=False,
    )
