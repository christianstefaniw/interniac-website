from django.urls import path

from .views import CareersPage, EditCareer, delete_career


urlpatterns = [
    path('', CareersPage.as_view(), name='careers'),
    path('delete/<int:career_id>/', delete_career, name='delete_career'),
    path('editcareer/<pk>', EditCareer.as_view(), name='edit_career')
]