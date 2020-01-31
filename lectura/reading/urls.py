from django.urls import include, path

from .views.views_project import ProjectView, ProjectsView
from .views.views_post import PostView
from .views.views_project_auth import (
    ProjectCreateView, ProjectUpdateView
)
from .views.views_post_auth import (
    AudioCreateView, PostCreateView, PostUpdateView
)

app_name = 'reading'

auth_urls = [
    path(
        'project/create/',
        ProjectCreateView.as_view(),
        name='project_create'
    ),
    path(
        'project/<int:project_pk>-<slug:project_slug>/update/',
        ProjectUpdateView.as_view(),
        name='project_update'
    ),
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
        'projects/',
        ProjectsView.as_view(),
        name='projects'
    ),
    path(
        'project/<int:project_pk>-<slug:project_slug>/',
        ProjectView.as_view(),
        name='project'
    ),
    path(
        'post/<int:post_pk>-<slug:post_slug>/',
        PostView.as_view(),
        name='post'
    ),
    path('auth/', include(auth_urls)),
]
