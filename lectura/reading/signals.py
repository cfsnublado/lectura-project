from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Post, ProjectMember


@receiver(post_delete, sender=ProjectMember)
def delete_related_posts(sender, instance=None, created=False, **kwargs):
    Post.objects.filter(creator=instance.member).delete()
