from django.contrib.auth import get_user_model
from django.views.generic import View

from core.views import AutocompleteMixin
from ..models import Project, ProjectMember

User = get_user_model()


class NonMemberAutocompleteView(AutocompleteMixin, View):
    """
    Autocomplete of users who are not
    members of specified project.
    """

    search_model = User
    search_field = "username"
    id_attr = "id"
    value_attr = "username"

    def get_queryset(self, **kwargs):
        qs = super(NonMemberAutocompleteView, self).get_queryset(**kwargs)
        project_pk = self.kwargs.get('project_pk', None)
        inner_qs = ProjectMember.objects
        if project_pk:
            try:
                project = Project.objects.get(id=project_pk)
                inner_qs = inner_qs.filter(project=project.id) \
                                   .select_related('project') \
                                   .values_list('member_id', flat=True)
                qs = qs.exclude(id__in=inner_qs) \
                       .exclude(id=project.owner_id) \
                       .exclude(id=self.request.user.id)
            except Project.DoesNotExist:
                qs = {}
        else:
            qs = {}
        return qs

    def set_label_attr(self, obj):
        return "{0}".format(obj.username)
