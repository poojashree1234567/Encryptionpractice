from django.urls import path
from .views import *

urlpatterns = [
    path('', UserProfileCreateView.as_view(), name='index'),
    path('profile/<uuid:uuid>/', UserprofileDetailView.as_view(), name='detail'),
    path('profiles/<uuid:uuid>/edit/', UserprofileEditView.as_view(), name='edit'),
    path('profile/<uuid:uuid>/delete/', UserprofileDeleteView.as_view(), name='delete'),
]