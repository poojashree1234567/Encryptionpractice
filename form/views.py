from django.shortcuts import render, redirect
from django.views import View
from .models import Userprofile, UserPhotos
from cryptography.fernet import Fernet
import base64
import uuid
from django.conf import settings
from .encrypt_decrypt import *

cipher_suite = Fernet(settings.FERNET_KEY)

class UserProfileCreateView(View):
    def get(self, request):
        userallprofiles = Userprofile.objects.all()
        context = {'userallprofiles': userallprofiles}
        return render(request, 'index.html', context)

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        gender = request.POST.get('gender')
        country = request.POST.get('country')
        image = request.FILES.get('image')

        profile_uuid = uuid.uuid4()
        # Create UserProfile object
        userprofileobj = Userprofile.objects.create(
            name=name,
            surname=surname,
            gender=gender,
            country=country,
            image=image,
            uuid=profile_uuid
        )

        # Handle multiple photos upload
        photos = request.FILES.getlist('photos')
        for photo in photos:
            photo_data = base64.b64encode(photo.read())
            UserPhotos.objects.create(user_profile=userprofileobj, photo=photo_data.decode())

        return redirect("/")

class UserprofileDetailView(View):
    def get(self, request, uuid):
        userprofileobj = Userprofile.objects.get(uuid=uuid)

        # Decrypt image data for display
        if userprofileobj.image:
            try:
                decrypted_image_data = cipher_suite.decrypt(userprofileobj.image)
                # decrypted_image_data = cipher_suite.decrypt(userprofileobj.image.encode())  # Decrypted data in bytes
                # decrypted_image_data = base64.b64decode(decrypted_image_data).decode()  # Convert bytes back to string if needed
            except Exception as e:
                print(f"Decryption error: {e}")

        context = {'userprofileobj': userprofileobj, 'decrypted_image_data': decrypted_image_data}
        return render(request, 'detail.html', context)

class UserprofileEditView(View):
    def get(self, request, encrypt_id):
        uuid = decrypt_message(encrypt_id)
        userprofileobj = Userprofile.objects.get(uuid=uuid)
        context = {'userprofileobj': userprofileobj}
        return render(request, 'edit.html', context)

    def post(self, request, uuid):
        userprofileobj = Userprofile.objects.get(uuid=uuid)
        userprofileobj.name = request.POST.get('name')
        userprofileobj.surname = request.POST.get('surname')
        userprofileobj.gender = request.POST.get('gender')
        userprofileobj.country = request.POST.get('country')

        if 'image' in request.FILES:
                image = request.FILES['image']
                image_data = base64.b64encode(image.read())  # Image data in bytes
                encrypted_image_data = cipher_suite.encrypt(image_data)  # Encrypted data in bytes
                userprofileobj.image = encrypted_image_data.decode()

        userprofileobj.save()

        # Handle multiple photos upload
        photos = request.FILES.getlist('photos')
        for photo in photos:
            photo_data = base64.b64encode(photo.read()) # Photo data in bytes
            UserPhotos.objects.create(user_profile=userprofileobj, photo=photo_data.decode())

        return redirect('detail', uuid=userprofileobj.uuid)

class UserprofileDeleteView(View):
    def post(self, request, uuid):
        print(uuid)
        userprofileobj = Userprofile.objects.get(uuid=uuid)
        userprofileobj.delete()
        return redirect('index')

