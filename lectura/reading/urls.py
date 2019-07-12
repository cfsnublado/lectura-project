from django.urls import include, path

from .views.views_entry_auth import (
    EntryCreateView
)

app_name = 'reading'

auth_urls = [
    path(
        'project/<int:project_pk>-<slug:project_slug>/entry/create/',
        EntryCreateView.as_view(),
        name='entry_create'
    ),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
]
