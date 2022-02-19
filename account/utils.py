from django.core.mail import send_mail
from django.core.mail import EmailMessage


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
    message = f"""
            Thank you for signing up.
            Please, activate your account.
            Activation link ;{activation_url}"""

    # send_mail(
    #     'Activate your account',
    #     message,
    #
    #     [email, ],
    #     fail_silently=False
    # )
    msg = EmailMessage(
        'Activate your account',
        body=message,
        to=[email, ]
    )
    msg.content_subtype = "html"
    msg.send()

