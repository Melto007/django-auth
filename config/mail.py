from django.core.mail import send_mail
from rest_framework import exceptions

def send_email(url, email):
    try:
        res = send_mail(
            subject='Reset Your Password',
            message="<a href='%s'>Click here</a> to reset your password" % url,
            from_email="from@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return res
    except Exception as e:
        print(e)
        raise exceptions.APIException('mail not send', e)