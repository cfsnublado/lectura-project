import getpass
import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.management.base import BaseCommand, CommandError

from project.models import Project
from ..utils import export_post


class Command(BaseCommand):
    help = 'Backs up posts in separate json files.'

    def login_user(self):
        username = input('Username: ')
        password = getpass.getpass('Password: ')

        user = authenticate(username=username, password=password)

        if user is not None:
            return user
        else:
            raise CommandError('Invalid login')

    def add_arguments(self, parser):
        parser.add_argument('--output_path', nargs=1, type=str)

    def handle(self, *args, **options):
        user = self.login_user()

        if options['output_path']:
            base_dir = Path(options['output_path'][0])
        else:
            base_dir = Path('{0}/docs/lectura_json/posts'.format(settings.BASE_DIR))
        base_dir.mkdir(parents=True, exist_ok=True)

        projects = Project.objects.filter(owner=user)

        for project in projects:
            project_dir = base_dir / project.slug
            project_dir.mkdir(parents=True, exist_ok=True)

            posts = project.posts.all()

            for post in posts:
                post_dict = export_post(post)
                filename = project_dir / '{0}.json'.format(post.slug)

                with filename.open('w+') as f:
                    f.write(json.dumps(post_dict, indent=2))
                    self.stdout.write(self.style.SUCCESS(filename))
