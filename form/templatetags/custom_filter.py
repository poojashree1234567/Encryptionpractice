from cryptography.fernet import Fernet
from django.conf import settings
from django import template

register = template.Library()

@register.filter(name='encrypt_id')
def encrypt_Id(message):
    f = Fernet(settings.DJANGO_ENCRYPTION_KEY)
    encrypted_message= f.encrypt(str(message).encode())
    print(encrypted_message)
    return encrypted_message.decode()