from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import (
    Post, ReadingProject, ReadingProjectMember
)
from ..permissions import (
    can_create_post_audio, can_delete_post, can_delete_project, can_edit_post,
    can_edit_project, is_post_creator, is_project_admin,
    is_project_author, is_project_editor, is_project_member,
    is_project_owner
)

User = get_user_model()


class TestCommon(TestCase):

    def setUp(self):
        self.pwd = 'Pizza?69p'
        self.user = User.objects.create_user(
            username='cfs',
            first_name='Christopher',
            last_name='Sanders',
            email='cfs7@cfs.com',
            password=self.pwd
        )
        self.admin = User.objects.create_user(
            username='naranjo',
            first_name='Naranjo',
            last_name='Oranges',
            email='naranjo@foo.com',
            password=self.pwd
        )
        self.editor = User.objects.create_user(
            username='manzano',
            first_name='Manzano',
            last_name='Apples',
            email='manzano@foo.com',
            password=self.pwd
        )
        self.author = User.objects.create_user(
            username='cerezo',
            first_name='Cerezo',
            last_name='Cherries',
            email='cerezo@foo.com',
            password=self.pwd
        )
        self.author_2 = User.objects.create_user(
            username='durazno',
            first_name='Durazano',
            last_name='Peaches',
            email='durazno@foo.com',
            password=self.pwd
        )
        self.non_member = User.objects.create_user(
            username='limonero',
            first_name='Limonero',
            last_name='Lemons',
            email='limonero@foo.com',
            password=self.pwd
        )
        self.project = ReadingProject.objects.create(
            owner=self.user,
            name='Some book',
            description='A good book'
        )
        ReadingProjectMember.objects.create(
            project=self.project,
            member=self.admin,
            role=ReadingProjectMember.ROLE_ADMIN
        )
        ReadingProjectMember.objects.create(
            project=self.project,
            member=self.editor,
            role=ReadingProjectMember.ROLE_EDITOR
        )
        ReadingProjectMember.objects.create(
            project=self.project,
            member=self.author,
            role=ReadingProjectMember.ROLE_AUTHOR
        )
        ReadingProjectMember.objects.create(
            project=self.project,
            member=self.author_2,
            role=ReadingProjectMember.ROLE_AUTHOR
        )


class ReadingProjectPermissionsTest(TestCommon):

    def test_is_project_owner(self):
        self.assertEqual(self.user, self.project.owner)
        self.assertTrue(is_project_owner(self.user, self.project))
        self.assertFalse(is_project_owner(self.admin, self.project))
        self.assertFalse(is_project_owner(self.editor, self.project))
        self.assertFalse(is_project_owner(self.author, self.project))

    def test_is_project_admin(self):
        # Owner
        self.assertTrue(is_project_admin(self.user, self.project))
        # Admin
        self.assertTrue(is_project_admin(self.admin, self.project))
        # Editor
        self.assertFalse(is_project_admin(self.editor, self.project))
        # Author
        self.assertFalse(is_project_admin(self.author, self.project))
        # Non member
        self.assertFalse(is_project_admin(self.non_member, self.project))

    def test_is_project_editor(self):
        # Owner
        self.assertTrue(is_project_editor(self.user, self.project))
        # Admin
        self.assertTrue(is_project_editor(self.admin, self.project))
        # Editor
        self.assertTrue(is_project_editor(self.editor, self.project))
        # Author
        self.assertFalse(is_project_editor(self.author, self.project))
        # Non member
        self.assertFalse(is_project_editor(self.non_member, self.project))

    def test_is_project_author(self):
        # Owner
        self.assertTrue(is_project_author(self.user, self.project))
        # Admin
        self.assertTrue(is_project_author(self.admin, self.project))
        # Editor
        self.assertTrue(is_project_author(self.editor, self.project))
        # Author
        self.assertTrue(is_project_author(self.author, self.project))
        # Non member
        self.assertFalse(is_project_author(self.non_member, self.project))

    def test_is_project_member(self):
        # Owner
        self.assertTrue(is_project_member(self.user, self.project))
        # Admin
        self.assertTrue(is_project_member(self.admin, self.project))
        # Editor
        self.assertTrue(is_project_member(self.editor, self.project))
        # Author
        self.assertTrue(is_project_member(self.author, self.project))
        # Non member
        self.assertFalse(is_project_member(self.non_member, self.project))

    def test_can_edit_project(self):
        # Owner
        self.assertTrue(can_edit_project(self.user, self.project))
        # Admin
        self.assertTrue(can_edit_project(self.admin, self.project))
        # Editor
        self.assertFalse(can_edit_project(self.editor, self.project))
        # Author
        self.assertFalse(can_edit_project(self.author, self.project))
        # Non member
        self.assertFalse(can_edit_project(self.non_member, self.project))

    def test_can_delete_project(self):
        # Owner
        self.assertTrue(can_delete_project(self.user, self.project))
        # Admin
        self.assertFalse(can_delete_project(self.admin, self.project))
        # Editor
        self.assertFalse(can_delete_project(self.editor, self.project))
        # Author
        self.assertFalse(can_delete_project(self.author, self.project))
        # Non member
        self.assertFalse(can_delete_project(self.non_member, self.project))


class PostPermissionsTest(TestCommon):

    def test_is_post_creator(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.author,
            name="Test post 1"
        )
        self.assertEqual(self.author, post.creator)
        self.assertTrue(is_post_creator(self.author, post))
        self.assertFalse(is_post_creator(self.editor, post))
        self.assertFalse(is_post_creator(self.admin, post))
        self.assertFalse(is_post_creator(self.user, post))

    def test_can_edit_post(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.author,
            name="Test post 1"
        )

        # Owner
        self.assertTrue(can_edit_post(self.user, post))
        # Admin
        self.assertTrue(can_edit_post(self.admin, post))
        # Editor
        self.assertTrue(can_edit_post(self.editor, post))
        # Author creator
        self.assertTrue(can_edit_post(self.author, post))
        # Non member
        self.assertFalse(can_edit_post(self.non_member, post))
        # Author non-creator
        self.assertFalse(can_edit_post(self.author_2, post))

    def test_can_delete_post(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.author,
            name="Test post 1"
        )

        # Owner
        self.assertTrue(can_delete_post(self.user, post))
        # Admin
        self.assertTrue(can_delete_post(self.admin, post))
        # Editor
        self.assertTrue(can_delete_post(self.editor, post))
        # Author creator
        self.assertTrue(can_delete_post(self.author, post))
        # Non member
        self.assertFalse(can_delete_post(self.non_member, post))
        # Author non-creator
        self.assertFalse(can_delete_post(self.author_2, post))


class PostAudioPermissionsTest(TestCommon):

    def test_can_create_post_audio(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.author,
            name="Test post 1"
        )

        # Owner
        self.assertTrue(can_create_post_audio(self.user, post))
        # Admin
        self.assertTrue(can_create_post_audio(self.admin, post))
        # Editor
        self.assertTrue(can_create_post_audio(self.editor, post))
        # Author creator
        self.assertTrue(can_create_post_audio(self.author, post))
        # Author non-creator
        self.assertTrue(can_create_post_audio(self.author_2, post))
        # Non member
        self.assertFalse(can_create_post_audio(self.non_member, post))
