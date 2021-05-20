from django.urls import path

from .views import CareersPage, EditCareer, delete_career

"""
`urlpatterns` for the accounts app  
Currently we support the following 3 urls:

1. **`/`** - view all careers
2. **`delete/<int:career_id>/`** - delete a career
3. **`editcareer/<pk>`** - edit a career

"""

urlpatterns = [
    path('', CareersPage.as_view(), name='careers'),
    path('delete/<int:career_id>/', delete_career, name='delete_career'),
    path('editcareer/<pk>', EditCareer.as_view(), name='edit_career')
]
