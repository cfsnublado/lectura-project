from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from dbx.conf import DbxConf
from security.conf import SecurityConf
from reading.conf import ReadingConf
from users.conf import ProfileConf

SECURITY_URL_PREFIX = SecurityConf.URL_PREFIX
READING_URL_PREFIX = ReadingConf.URL_PREFIX
USER_URL_PREFIX = ProfileConf.URL_PREFIX
DBX_URL_PREFIX = DbxConf.URL_PREFIX

urlpatterns = i18n_patterns(
    path("", include("social_django.urls", namespace="social")),
    path('', include("core.urls", namespace="core")),
    path('', include('app.urls')),
    path('api/', include('app.api.urls', namespace='api')),
    path('djangoadmin/', admin.site.urls),
    path('{0}/'.format(SECURITY_URL_PREFIX), include('security.urls', namespace='security')),
    path('{0}/'.format(USER_URL_PREFIX), include('users.urls', namespace='users')),
    path('{0}/'.format(READING_URL_PREFIX), include('reading.urls', namespace='reading')),
    path('{0}/'.format(DBX_URL_PREFIX), include('dbx.urls', namespace='dbx')),

    prefix_default_language=False
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
