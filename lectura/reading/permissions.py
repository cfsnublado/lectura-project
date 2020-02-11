from .models import ReadingProjectMember


def is_project_owner(user, project):
    return user.id == project.owner_id


def is_project_role(user, project, role):
    if is_project_owner(user, project):
        return True
    elif role in (i[0] for i in ReadingProjectMember.ROLE_CHOICES):
        member = project.get_member(user)
        return bool(member and member.role >= role)
    else:
        return False


def is_project_admin(user, project):
    return is_project_role(user, project, ReadingProjectMember.ROLE_ADMIN)


def is_project_editor(user, project):
    return is_project_role(user, project, ReadingProjectMember.ROLE_EDITOR)


def is_project_author(user, project):
    return is_project_role(user, project, ReadingProjectMember.ROLE_AUTHOR)


def is_project_member(user, project):
    return bool(is_project_owner(user, project) or project.get_member(user))


def is_post_creator(user, post):
    return user.id == post.creator_id


def can_create_post(user, project):
    """
    Project owner, Project member: yes
    """
    return is_project_member(user, project)


def can_edit_post(user, post):
    """
    Project Owner, Admin, Editor: yes
    Author: yes, if post creator
    """
    project = post.project
    can_edit = False

    if is_project_owner(user, project):
        can_edit = True
    else:
        member = project.get_member(user)
        if member:
            if member.role >= ReadingProjectMember.ROLE_EDITOR:
                can_edit = True
            elif member.role == ReadingProjectMember.ROLE_AUTHOR and is_post_creator(user, post):
                can_edit = True

    return can_edit


def can_delete_post(user, post):
    """
    Project Owner, Admin: yes
    Editor, Author: yes, if post creator
    """
    project = post.project
    can_delete = False

    if is_project_owner(user, project):
        can_delete = True
    else:
        member = project.get_member(user)
        if member:
            if member.role >= ReadingProjectMember.ROLE_ADMIN:
                can_delete = True
            elif member.role >= ReadingProjectMember.ROLE_AUTHOR and is_post_creator(user, post):
                can_delete = True

    return can_delete
