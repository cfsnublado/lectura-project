
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from django.urls import path
from django.conf.urls import include

from users.api.views_api import UserViewSet, ProfileViewSet
from reading.api.views_project import ProjectViewSet
from reading.api.views_reading import NestedReadingViewSet, ReadingViewSet

app_name = 'app'

router = DefaultRouter()

# users
router.register('user', UserViewSet, base_name='user')
router.register('profile', ProfileViewSet, base_name='profile')

# reading
router.register('project', ProjectViewSet, base_name='project')
router.register('reading', ReadingViewSet, base_name='reading')

reading_router = NestedSimpleRouter(router, 'project', lookup='project')
reading_router.register('reading', NestedReadingViewSet, base_name='nested-reading')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='auth_token'),
    path('', include(router.urls)),
    path('', include(reading_router.urls)),
]
