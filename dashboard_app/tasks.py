# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.http import HttpRequest
from .views.notifications import create_notification
# from twilio.rest import Client


@shared_task
def run_create_notification():
    request = HttpRequest()
    create_notification(request)
    send_email_task.delay(
        "mrdehan2014@gmail.com", "Notification Subject", "Notification Body"
    )
    # send_sms_task.delay("+1234567890", "Notification SMS Body")


@shared_task
def send_email_task(recipient_email, subject, message):
    send_mail(
        subject,
        message,
        "mrdehan2017@gmail.com",  # Replace with your "from" email address
        [recipient_email],
        fail_silently=False,
    )


# @shared_task
# def send_sms_task(phone_number, message):
#     account_sid = "your_twilio_account_sid"
#     auth_token = "your_twilio_auth_token"
#     client = Client(account_sid, auth_token)
#     client.messages.create(
#         body=message,
#         from_="+your_twilio_phone_number",  # Replace with your Twilio phone number
#         to=phone_number,
#     )
