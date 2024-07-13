
from cryptography.fernet import Fernet
from django.conf import settings

def decrypt_message(encrypted_message):
    f = Fernet(settings.DJANGO_ENCRYPTION_KEY)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message