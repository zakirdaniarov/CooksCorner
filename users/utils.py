from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


def send_activation_email(request, user):
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relative_link = reverse('email-verification')
    abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
    subject = 'Verify your email'
    message = 'Hi ' + user.username + \
        ' Use the link below to verify your email \n' + abs_url
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)
