from django.urls import include, path

from .views.views_post import PostView
from .views.views_post_auth import (
    AudioCreateView, PostCreateView, PostUpdateView
)

app_name = 'reading'

auth_urls = [
    path(
        'project/<int:project_pk>-<slug:project_slug>/post/create/',
        PostCreateView.as_view(),
        name='post_create'
    ),
    path(
        'post/<int:post_pk>-<slug:post_slug>/update/',
        PostUpdateView.as_view(),
        name='post_update'
    ),
    path(
        'post/<int:post_pk>-<slug:post_slug>/audio/create/',
        AudioCreateView.as_view(),
        name='audio_create'
    ),
]

urlpatterns = [
    path(
        'post/<int:post_pk>-<slug:post_slug>/',
        PostView.as_view(),
        name='post'
    ),
    path('auth/', include(auth_urls)),
]
