from django.urls import include, path

from .views.views_entry import EntryView
from .views.views_entry_auth import (
    EntryCreateView, EntryUpdateView
)

app_name = 'reading'

auth_urls = [
    path(
        'project/<int:project_pk>-<slug:project_slug>/entry/create/',
        EntryCreateView.as_view(),
        name='entry_create'
    ),
    path(
        'entry/<int:entry_pk>-<slug:entry_slug>/update/',
        EntryUpdateView.as_view(),
        name='entry_update'
    ),
]

urlpatterns = [
    path(
        'entry/<int:entry_pk>-<slug:entry_slug>/',
        EntryView.as_view(),
        name='entry'
    ),
    path('auth/', include(auth_urls)),
]
