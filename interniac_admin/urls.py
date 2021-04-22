from django.urls import path

from .views import CareerInfoFormView, UserInfo, AllUsers, delete_account

urlpatterns = [
    path('createcareer/', CareerInfoFormView.as_view(), name='create_career_info'),
    path('allusers/', AllUsers.as_view(), name='all_users'),
    path('userinfo/<slug>', UserInfo.as_view(), name='user_info'),
    path('delete/<int:id>', delete_account, name='delete_account')
]