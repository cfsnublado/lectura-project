from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import (
    Post, ReadingProject, ReadingProjectMember
)
from ..permissions import (
    can_delete_post, can_delete_project, can_edit_post,
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
        self.user_2 = User.objects.create_user(
            username='naranjo',
            first_name='Naranjo',
            last_name='Oranges',
            email='naranjo@foo.com',
            password=self.pwd
        )
        self.user_3 = User.objects.create_user(
            username='manzano',
            first_name='Manzano',
            last_name='Apples',
            email='manzano@foo.com',
            password=self.pwd
        )
        self.user_4 = User.objects.create_user(
            username='cerezo',
            first_name='Cerezo',
            last_name='Cherries',
            email='cerezo@foo.com',
            password=self.pwd
        )
        self.user_5 = User.objects.create_user(
            username='limonero',
            first_name='Limonero',
            last_name='Lemons',
            email='limonero@foo.com',
            password=self.pwd
        )
        self.user_6 = User.objects.create_user(
            username='durazno',
            first_name='Durazano',
            last_name='Peaches',
            email='durazno@foo.com',
            password=self.pwd
        )
        self.project = ReadingProject.objects.create(
            owner=self.user,
            name='Some book',
            description='A good book'
        )
        self.author = ReadingProjectMember.objects.create(
            project=self.project,
            member=self.user_2,
            role=ReadingProjectMember.ROLE_AUTHOR
        )
        self.author_2 = ReadingProjectMember.objects.create(
            project=self.project,
            member=self.user_6,
            role=ReadingProjectMember.ROLE_AUTHOR
        )
        self.editor = ReadingProjectMember.objects.create(
            project=self.project,
            member=self.user_3,
            role=ReadingProjectMember.ROLE_EDITOR
        )
        self.admin = ReadingProjectMember.objects.create(
            project=self.project,
            member=self.user_4,
            role=ReadingProjectMember.ROLE_ADMIN
        )


class ReadingProjectPermissionsTest(TestCommon):

    def test_is_project_owner(self):
        self.assertEqual(self.user, self.project.owner)
        self.assertTrue(is_project_owner(self.user, self.project))

    def test_is_project_admin(self):
        # Owner
        self.assertTrue(is_project_admin(self.user, self.project))
        # Admin
        self.assertTrue(is_project_admin(self.admin.member, self.project))
        # Editor
        self.assertFalse(is_project_admin(self.editor.member, self.project))
        # Author
        self.assertFalse(is_project_admin(self.author.member, self.project))
        # Non member
        self.assertFalse(is_project_admin(self.user_5, self.project))

    def test_is_project_editor(self):
        # Owner
        self.assertTrue(is_project_editor(self.user, self.project))
        # Admin
        self.assertTrue(is_project_editor(self.admin.member, self.project))
        # Editor
        self.assertTrue(is_project_editor(self.editor.member, self.project))
        # Author
        self.assertFalse(is_project_editor(self.author.member, self.project))
        # Non member
        self.assertFalse(is_project_editor(self.user_5, self.project))

    def test_is_project_author(self):
        # Owner
        self.assertTrue(is_project_author(self.user, self.project))
        # Admin
        self.assertTrue(is_project_author(self.admin.member, self.project))
        # Editor
        self.assertTrue(is_project_author(self.editor.member, self.project))
        # Author
        self.assertTrue(is_project_author(self.author.member, self.project))
        # Non member
        self.assertFalse(is_project_author(self.user_5, self.project))

    def test_is_project_member(self):
        # Owner
        self.assertTrue(is_project_member(self.user, self.project))
        # Admin
        self.assertTrue(is_project_member(self.admin.member, self.project))
        # Editor
        self.assertTrue(is_project_member(self.editor.member, self.project))
        # Author
        self.assertTrue(is_project_member(self.author.member, self.project))
        # Non member
        self.assertFalse(is_project_member(self.user_5, self.project))

    def test_can_edit_project(self):
        # Owner
        self.assertTrue(can_edit_project(self.user, self.project))
        # Admin
        self.assertTrue(can_edit_project(self.admin.member, self.project))
        # Editor
        self.assertFalse(can_edit_project(self.editor.member, self.project))
        # Author
        self.assertFalse(can_edit_project(self.author.member, self.project))
        # Non member
        self.assertFalse(can_edit_project(self.user_5, self.project))

    def test_can_delete_project(self):
        # Owner
        self.assertTrue(can_delete_project(self.user, self.project))
        # Admin
        self.assertFalse(can_delete_project(self.admin.member, self.project))
        # Editor
        self.assertFalse(can_delete_project(self.editor.member, self.project))
        # Author
        self.assertFalse(can_delete_project(self.author.member, self.project))
        # Non member
        self.assertFalse(can_delete_project(self.user_5, self.project))


class PostPermissionsTest(TestCommon):

    def test_is_post_creator(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.user_2,
            name="Test post 1"
        )
        self.assertEqual(self.user_2, post.creator)
        self.assertTrue(is_post_creator(self.user_2, post))

    def test_can_edit_post(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.author.member,
            name="Test post 1"
        )

        # Owner
        self.assertTrue(can_edit_post(self.user, post))
        # Admin
        self.assertTrue(can_edit_post(self.admin.member, post))
        # Editor
        self.assertTrue(can_edit_post(self.editor.member, post))
        # Author creator
        self.assertTrue(can_edit_post(self.author.member, post))
        # Non member
        self.assertFalse(can_edit_post(self.user_5, post))
        # Author non-creator
        self.assertFalse(can_edit_post(self.author_2.member, post))

    def test_can_delete_post(self):
        post = Post.objects.create(
            project=self.project,
            creator=self.author.member,
            name="Test post 1"
        )

        # Owner
        self.assertTrue(can_delete_post(self.user, post))
        # Admin
        self.assertTrue(can_delete_post(self.admin.member, post))
        # Editor
        self.assertTrue(can_delete_post(self.editor.member, post))
        # Author creator
        self.assertTrue(can_delete_post(self.author.member, post))
        # Non member
        self.assertFalse(can_delete_post(self.user_5, post))
        # Author non-creator
        self.assertFalse(can_delete_post(self.author_2.member, post))