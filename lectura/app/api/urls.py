
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from django.urls import path
from django.conf.urls import include

from dbx.api.views_api import (
    DbxDeleteFileView, DbxSharedLinkView,
    DbxUploadAudioView, DbxUserFilesView
)
from users.api.views_api import UserViewSet, ProfileViewSet
from reading.api.views_project import ProjectViewSet, ProjectImportView
from reading.api.views_project_member import (
    NestedProjectMemberViewSet, ProjectMemberViewSet
)
from reading.api.views_post import (
    NestedPostAudioViewSet, NestedPostViewSet,
    PostViewSet, PostAudioViewSet, PostExportView, PostImportView
)

app_name = "app"

router = DefaultRouter()

# users
router.register("user", UserViewSet, basename="user")
router.register("profile", ProfileViewSet, basename="profile")

# project
router.register("project", ProjectViewSet, basename="project")

# project member
router.register(
    "project-member",
    ProjectMemberViewSet,
    basename="project-member"
)
project_member_router = NestedSimpleRouter(
    router,
    "project",
    lookup="project"
)
project_member_router.register(
    "project-member",
    NestedProjectMemberViewSet,
    basename="nested-project-member"
)

# post
router.register("post", PostViewSet, basename="post")
post_router = NestedSimpleRouter(router, "project", lookup="project")
post_router.register("post", NestedPostViewSet, basename="nested-post")

# post audio
router.register("post-audio", PostAudioViewSet, basename="post-audio")
post_audio_router = NestedSimpleRouter(router, "post", lookup="post")
post_audio_router.register(
    "post-audio",
    NestedPostAudioViewSet,
    basename="nested-post-audio"
)

urlpatterns = [
    path("api-token-auth/", views.obtain_auth_token, name="auth_token"),
    path(
        "reading/project/import/",
        ProjectImportView.as_view(),
        name="project_import"
    ),
    path("reading/post/import/", PostImportView.as_view(), name="post_import"),
    path(
        "reading/post/<int:post_pk>/export/",
        PostExportView.as_view(),
        name="post_export"
    ),
    path("dbx-shared-link/", DbxSharedLinkView.as_view(), name="dbx_shared_link"),
    path("dbx-user-files/", DbxUserFilesView.as_view(), name="dbx_user_files"),
    path("dbx-delete-file/", DbxDeleteFileView.as_view(), name="dbx_delete_file"),
    path("dbx-upload-audio/", DbxUploadAudioView.as_view(), name="dbx_upload_audio"),

    path("", include(router.urls)),
    path("", include(project_member_router.urls)),
    path("", include(post_router.urls)),
    path("", include(post_audio_router.urls)),
]
