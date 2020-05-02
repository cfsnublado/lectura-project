import json
from builtins import FileExistsError
from pathlib import Path

from django.conf import settings

from core.management.base import LoginCommand
from reading.models import Post
from reading.utils import export_post


class Command(LoginCommand):
    help = "Backs up a user's posts in respective json files."

    def add_arguments(self, parser):
        parser.add_argument('--output_path', nargs=1, type=str)

    def handle(self, *args, **options):
        user = self.login_user()

        if options['output_path']:
            base_dir = Path(options['output_path'][0])
        else:
            base_dir = Path('{0}/docs/lectura_json/posts'.format(settings.BASE_DIR))

        base_dir.mkdir(parents=True, exist_ok=True)
        posts = Post.objects.filter(creator=user).select_related('project', 'creator')

        for post in posts:
            project_dir = base_dir / post.project.slug
            try:
                project_dir.mkdir(parents=True, exist_ok=False)
            except FileExistsError:
                pass
            post_filename = project_dir / '{0}.json'.format(post.slug)
            post_dict = export_post(post)

            with post_filename.open('w+') as f:
                f.write(json.dumps(post_dict, indent=2))
                self.stdout.write(self.style.SUCCESS(post_filename))
