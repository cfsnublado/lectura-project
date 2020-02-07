import getpass
import json
from pathlib import Path

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.management.base import BaseCommand, CommandError

from project.models import Project
from ..utils import export_project


class Command(BaseCommand):
    help = 'Backs up a project and its posts in a single json file.'

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
            base_dir = Path('{0}/docs/lectura_json/projects'.format(settings.BASE_DIR))
        base_dir.mkdir(parents=True, exist_ok=True)

        projects = Project.objects.filter(owner=user)

        for project in projects:
            project_dir = base_dir / project.slug
            project_dir.mkdir(parents=True, exist_ok=True)
            project_filename = project_dir / '{0}.json'.format(project.slug)
            project_dict = export_project(project)

            with project_filename.open('w+') as f:
                f.write(json.dumps(project_dict, indent=2))
                self.stdout.write(self.style.SUCCESS(project_filename))
