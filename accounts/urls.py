from django.urls import path

from accounts.views import Profile, delete_user

urlpatterns = [
    path('profile/', Profile.as_view(), name='profile'),
    path('delete/<int:id>', delete_user, name='delete'),
]
