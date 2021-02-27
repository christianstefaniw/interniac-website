from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import *
from home import urls as home_urls
from careers.views import CareersPage
from aboutus.views import AboutUsPage
from authentication import urls as auth_urls
from accounts import urls as accounts_urls
from marketplace import urls as marketplace_urls
from applications import urls as application_urls


urlpatterns = [
    path('', include(home_urls)),
    path('careers/', CareersPage.as_view(), name='careers'),
    path('aboutus/', AboutUsPage.as_view(), name='aboutus'),
    path('success/', success, name='success'),
    path('error/', error, name='error'),
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urls)),
    path('auth/', include(auth_urls)),
    path('marketplace/', include(marketplace_urls)),
    path('applications/', include(application_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'connect_x.views.Error404Handler'

