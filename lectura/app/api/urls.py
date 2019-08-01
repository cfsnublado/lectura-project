
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from django.urls import path
from django.conf.urls import include

from dbx.api.views_api import (
    DbxSharedLinkView, DbxUploadAudioView, DbxUserFilesView
)
from users.api.views_api import UserViewSet, ProfileViewSet
from reading.api.views_project import ProjectViewSet, ProjectImportView
from reading.api.views_post import (
    NestedPostViewSet, PostViewSet, PostExportView,
    PostImportView
)

app_name = 'app'

router = DefaultRouter()

# users
router.register('user', UserViewSet, base_name='user')
router.register('profile', ProfileViewSet, base_name='profile')

# post
router.register('project', ProjectViewSet, base_name='project')
router.register('post', PostViewSet, base_name='post')

post_router = NestedSimpleRouter(router, 'project', lookup='project')
post_router.register('post', NestedPostViewSet, base_name='nested-post')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='auth_token'),
    path('reading/project/import/', ProjectImportView.as_view(), name='project_import'),
    path('reading/post/import/', PostImportView.as_view(), name='post_import'),
    path(
        'reading/post/<int:post_pk>/export/',
        PostExportView.as_view(),
        name='post_export'
    ),
    path('dbx-shared-link/', DbxSharedLinkView.as_view(), name='dbx_shared_link'),
    path('dbx-user-files/', DbxUserFilesView.as_view(), name='dbx_user_files'),
    path('dbx-upload-audio/', DbxUploadAudioView.as_view(), name='dbx_upload_audio'),

    path('', include(router.urls)),
    path('', include(post_router.urls)),
]
