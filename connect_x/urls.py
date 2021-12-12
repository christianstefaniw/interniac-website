from notifications import urls as notify_urls

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from connect_x.views import success, error, terms_and_conditions
from home import urls as home_urls
from authentication import urls as auth_urls
from accounts import urls as accounts_urls
from marketplace import urls as marketplace_urls
from applications import urls as application_urls
from careers import urls as careers_urls
from aboutus import urls as aboutus_urls
from interniac_admin import urls as interniac_admin_urls
from stats import urls as stats_urls

urlpatterns = [
    path('', include(home_urls)),
    url('^inbox/notifications/', include(notify_urls, namespace='notifications')),
    path('termsandconditions/', terms_and_conditions,
         name='terms_and_conditions'),
    path('careers/', include(careers_urls)),
    path('aboutus/', include(aboutus_urls)),
    path('success/', success, name='success'),
    path('error/', error, name='error'),
    path('management/', admin.site.urls),
    path('management/defender/', include('defender.urls')),
    path('interniacadmin/', include(interniac_admin_urls)),
    path('accounts/', include(accounts_urls)),
    path('auth/', include(auth_urls)),
    path('marketplace/', include(marketplace_urls)),
    path('applications/', include(application_urls)),
    path('stats/', include(stats_urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = 'connect_x.views.error_500'
handler404 = 'connect_x.views.error_404'
