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


def can_edit_project(user, project):
    return is_project_admin(user, project)


def can_delete_project(user, project):
    return is_project_owner(user, project)


def is_post_creator(user, post):
    return user.id == post.creator_id


def can_create_post(user, project):
    return is_project_member(user, project)


def can_edit_post(user, post):
    """
    True: Project Owner, Admin, Editor, Author (post creator)
    False: Author (not post creator)
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
    True: Project Owner, Admin, Editor, Author (post creator)
    False: Author (not post creator)
    """
    return can_edit_post(user, post)


def can_create_post_audio(user, post):
    return is_project_member(user, post.project)
