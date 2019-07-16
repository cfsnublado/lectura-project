from django.urls import path
from django.conf.urls import include

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from users.api.views_api import UserViewSet, ProfileViewSet
from reading.api.views_project import ProjectViewSet
from reading.api.views_reading import ReadingViewSet

app_name = 'app'

router = DefaultRouter()

# users
router.register('user', UserViewSet, base_name='user')
router.register('profile', ProfileViewSet, base_name='profile')

# reading
router.register('project', ProjectViewSet, base_name='project')
router.register('reading', ReadingViewSet, base_name='reading')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token, name='auth_token'),
    path('', include(router.urls)),
]
