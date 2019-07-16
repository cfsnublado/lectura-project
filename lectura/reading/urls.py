from django.urls import include, path

from .views.views_reading import ReadingView
from .views.views_reading_auth import (
    ReadingCreateView, ReadingUpdateView
)

app_name = 'reading'

auth_urls = [
    path(
        'project/<int:project_pk>-<slug:project_slug>/reading/create/',
        ReadingCreateView.as_view(),
        name='reading_create'
    ),
    path(
        'reading/<int:reading_pk>-<slug:reading_slug>/update/',
        ReadingUpdateView.as_view(),
        name='reading_update'
    ),
]

urlpatterns = [
    path(
        'reading/<int:reading_pk>-<slug:reading_slug>/',
        ReadingView.as_view(),
        name='reading'
    ),
    path('auth/', include(auth_urls)),
]
