from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_code(email, activation_code):
    activation_link = f'http://localhost:8000/account/activate/{activation_code}/'
    message = f"""
               Hello! Thank you for joined our family. \n  

               Activate your account with a link: \n {activation_link}
               """
    send_mail("Activate account", message, 'admin@admin.com', recipient_list=[email])

