from django.urls import include, path

from .views.views_reading_autocomplete import (
    NonMemberAutocompleteView
)
from .views.views_project import ProjectsView, ProjectView
from .views.views_project_auth import (
    ProjectCreateView, ProjectsView as ProjectsAuthView,
    ProjectUpdateView
)
from .views.views_post import (
    PostView, PostAudiosView
)
from .views.views_project_member_auth import (
    ProjectMemberCreateView, ProjectMemberUpdateView,
    ProjectMembersView as ProjectMembersAuthView
)
from .views.views_post_auth import (
    PostAudioCreateView, PostAudioUpdateView,
    PostCreateView, PostUpdateView
)

app_name = 'reading'

auth_urls = [
    path(
        'projects/',
        ProjectsAuthView.as_view(),
        name='projects_auth'
    ),
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
        'project/<int:project_pk>-<slug:project_slug>/project-members/',
        ProjectMembersAuthView.as_view(),
        name='project_members_auth'
    ),
    path(
        'project/<int:project_pk>-<slug:project_slug>/project-member/create',
        ProjectMemberCreateView.as_view(),
        name='project_member_create'
    ),
    path(
        'project-member/<int:pk>/update',
        ProjectMemberUpdateView.as_view(),
        name='project_member_update'
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
        PostAudioCreateView.as_view(),
        name='post_audio_create'
    ),
    path(
        'post-audio/<int:pk>/update/',
        PostAudioUpdateView.as_view(),
        name='post_audio_update'
    ),
]

urlpatterns = [
    path(
        'autocomplete/nonmember/project/<int:project_pk>/',
        NonMemberAutocompleteView.as_view(),
        name="project_nonmember_autocomplete"
    ),
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
    path(
        'post/<int:post_pk>-<slug:post_slug>/audios/',
        PostAudiosView.as_view(),
        name='post_audios'
    ),
    path('auth/', include(auth_urls)),
]
