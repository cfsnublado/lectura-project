from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import resolve, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView
)

from core.views import (
    MessageMixin
)
from ..conf import settings
from ..forms import PostCreateForm
from ..models import Post, ReadingProject, ReadingProjectMember
from ..views.views_mixins import (
    ProjectMixin, ProjectMemberMixin,
    ProjectSessionMixin
)
from ..views.views_post_auth import PostCreateView

User = get_user_model()

APP_NAME = 'reading'
URL_PREFIX = getattr(settings, 'READING_URL_PREFIX')


class TestCommon(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.pwd = 'Pizza?69p'
        self.user = User.objects.create_user(
            username='cfs7',
            first_name='Christopher',
            last_name='Sanders',
            email='cfs7@foo.com',
            password=self.pwd
        )
        self.project = ReadingProject.objects.create(
            owner=self.user,
            name='test project'
        )
        self.admin = User.objects.create_user(
            username='admin7',
            first_name='Admin',
            last_name='Admin',
            email='admin7@foo.com',
            password=self.pwd
        )
        ReadingProjectMember.objects.create(
            member=self.admin,
            project=self.project,
            role=ReadingProjectMember.ROLE_ADMIN
        )
        self.editor = User.objects.create_user(
            username='editor7',
            first_name='Editor',
            last_name='Editor',
            email='editor7@foo.com',
            password=self.pwd
        )
        ReadingProjectMember.objects.create(
            member=self.editor,
            project=self.project,
            role=ReadingProjectMember.ROLE_EDITOR
        )
        self.author_1 = User.objects.create_user(
            username='author1',
            first_name='AuthorOne',
            last_name='AuthorOne',
            email='author_1@foo.com',
            password=self.pwd
        )
        ReadingProjectMember.objects.create(
            member=self.author_1,
            project=self.project,
            role=ReadingProjectMember.ROLE_AUTHOR
        )
        self.author_2 = User.objects.create_user(
            username='author2',
            first_name='AuthorTwo',
            last_name='AuthorTwo',
            email='author_2@foo.com',
            password=self.pwd
        )
        ReadingProjectMember.objects.create(
            member=self.author_2,
            project=self.project,
            role=ReadingProjectMember.ROLE_AUTHOR
        )
        self.non_member = User.objects.create_user(
            username='nonmember7',
            first_name='Nonmember',
            last_name='Nonmember',
            email='nonmember7@foo.com',
            password=self.pwd
        )

    def login_test_user(self, username=None):
        self.client.login(username=username, password=self.pwd)

    def add_session_to_request(self, request):
        '''Annotate a request object with a session'''
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()


class PostCreateViewTest(TestCommon):

    def setUp(self):
        super(PostCreateViewTest, self).setUp()
        self.post_data = {
            'name': 'test post',
            'description': 'Oh yeah.',
            'content': 'oh yeah'
        }

    def test_inheritance(self):
        classes = (
            LoginRequiredMixin,
            ProjectMixin,
            ProjectMemberMixin,
            ProjectSessionMixin,
            MessageMixin,
            CreateView
        )
        for class_name in classes:
            self.assertTrue(issubclass(PostCreateView, class_name))

    def test_correct_view_used(self):
        found = resolve(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(found.func.__name__, PostCreateView.as_view().__name__)

    def test_view_non_authenticated_user_redirected_to_login(self):
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertRedirects(
            response,
            expected_url='{0}?next=/{1}/auth/project/{2}-{3}/post/create/'.format(
                reverse(settings.LOGIN_URL),
                URL_PREFIX,
                self.project.id,
                self.project.slug
            ),
            status_code=302,
            target_status_code=200,
            msg_prefix=''
        )

    def test_view_returns_correct_status_code(self):
        self.login_test_user(self.user.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template(self):
        self.login_test_user(self.user.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertTemplateUsed(response, '{0}/auth/post_create.html'.format(APP_NAME))

    def test_view_uses_correct_form(self):
        self.login_test_user(self.user.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertIsInstance(response.context['form'], PostCreateForm)

    def test_view_injects_form_kwargs(self):
        self.login_test_user(self.user.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        form = response.context['form']
        self.assertEqual(form.project, self.project)
        self.assertEqual(form.creator, self.user)

    def test_view_creates_object(self):
        self.login_test_user(self.user.username)
        self.assertFalse(
            Post.objects.filter(
                creator=self.user,
                name=self.post_data['name'],
                content=self.post_data['content']
            ).exists()
        )
        self.client.post(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            ),
            self.post_data
        )
        self.assertTrue(
            Post.objects.filter(
                creator=self.user,
                name=self.post_data['name'],
                content=self.post_data['content']
            ).exists()
        )

    def test_invalid_data_shows_form_errors_and_does_not_save(self):
        self.post_data['name'] = ''
        self.login_test_user(self.user.username)
        response = self.client.post(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            ),
            self.post_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Post.objects.filter(
                name=self.post_data['name'],
                content=self.post_data['content']
            ).exists()
        )
        self.assertIsInstance(response.context['form'], PostCreateForm)
        self.assertFormError(response, 'form', 'name', _('validation_field_required'))

    def test_view_redirects_on_success(self):
        self.login_test_user(self.user.username)
        response = self.client.post(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            ),
            self.post_data
        )
        post = Post.objects.get(
            name=self.post_data['name']
        )
        self.assertRedirects(
            response,
            expected_url=reverse(
                'reading:post',
                kwargs={
                    'post_pk': post.id,
                    'post_slug': post.slug
                }
            ),
            status_code=302,
            target_status_code=200,
            msg_prefix=''
        )

    def test_view_permissions(self):
        self.login_test_user(self.user.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.login_test_user(self.admin.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.login_test_user(self.editor.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.login_test_user(self.author_1.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(response.status_code, 200)

        self.client.logout()
        self.login_test_user(self.non_member.username)
        response = self.client.get(
            reverse(
                'reading:post_create',
                kwargs={
                    'project_pk': self.project.id,
                    'project_slug': self.project.slug
                }
            )
        )
        self.assertEqual(response.status_code, 403)
