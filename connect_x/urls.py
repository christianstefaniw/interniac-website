from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import *
from home import urls as home_urls
from careers.views import CareersPage
from aboutus.views import AboutUsPage
from registration import urls as registration_urls
from accounts import urls as accounts_urls
from marketplace import urls as marketplace_urls

urlpatterns = [
    path('', include(home_urls)),
    path('careers/', CareersPage.as_view(), name='careers'),
    path('aboutus/', AboutUsPage.as_view(), name='aboutus'),
    path('success/', success, name='success'),
    path('error/', error, name='error'),
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urls)),
    path('auth/', include(registration_urls)),
    path('marketplace/', include(marketplace_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'connect_x.views.Error404Handler'

