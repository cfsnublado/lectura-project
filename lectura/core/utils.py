import markdown2

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader
from django.urls import reverse
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.functional import keep_lazy, Promise
from django.utils.http import urlsafe_base64_encode


def markdown_to_html(text, strip_outer_tags=False, extras=['fenced-code-blocks']):
    if not text:
        return ''
    html = markdown2.markdown(text, extras=extras)
    if strip_outer_tags:
        html = strip_outer_html_tags(html)
    return html


def strip_outer_html_tags(s):
    ''' strips outer html tags '''

    start = s.find('>') + 1
    end = len(s) - s[::-1].find('<') - 1
    return s[start:end]


def print_color(color_code, text):
    '''
    Prints in color to the console according to the integer color code.

    color codes:
        91: red
        92: green
        93: yellow
        94: light purple
        95: purple
        96: cyan
        97: light gray
        98: black
    '''
    print('\033[{0}m {1}\033[00m'.format(color_code, text))


def setup_test_view(view, request, *args, **kwargs):
    '''
    view - CBV instance
    request - RequestFactory request
    '''
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class FuzzyInt(int):
    '''A fuzzy integer between two integers, inclusive. Useful for testing.
    Example: FuzzyInt(5, 8) A value between 5 and 8, inclusive.
    '''
    def __new__(cls, lowest, highest):
        obj = super(FuzzyInt, cls).__new__(cls, highest)
        obj.lowest = lowest
        obj.highest = highest
        return obj

    def __eq__(self, other):
        return other >= self.lowest and other <= self.highest

    def __repr__(self):
        return '[%d..%d]' % (self.lowest, self.highest)


# Application utilities
@keep_lazy(six.text_type)
def format_lazy(string, *args, **kwargs):
    return string.format(*args, **kwargs)


def send_user_token_email(
    user=None,
    request=None,
    subject_template_name=None,
    from_email=None,  # settings.EMAIL_HOST_USER,
    email_template_name=None,
    html_email_template_name=None,
    token_generator=default_token_generator,
    site_name=None,
    site_url=None,
    extra_email_context=None
):
    '''Sends an email to a user with a uid/token link to reset password.

    user - existing user in db
    request - request from view where function is called
    subject_template_name - text file containing the email subject
    from_email - email address of sender
    email_template_name - template containing email body
    html_email_template - html-formatted template to display email_template
    token_generator - generate token based on user
    site name - name of project
    site_url - main project url
    extra_email_context - dict containing extra email context variables
    '''
    if not user or not request or not subject_template_name or not email_template_name:
        pass
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    token_url = request.build_absolute_uri(
        reverse(
            'users:user_forgot_password_reset',
            kwargs={'uidb64': uid, 'token': token}
        )
    )
    if site_name is None:
        if hasattr(settings, 'PROJECT_NAME'):
            site_name = settings.PROJECT_NAME
    if site_url is None:
        if hasattr(settings, 'PROJECT_HOME_URL'):
            site_url = request.build_absolute_uri(reverse(settings.PROJECT_HOME_URL))
        else:
            site_url = request.build_absolute_uri('/')
    else:
        site_url = request.build_absolute_uri(reverse(site_url))
    context = {
        'request': request,
        'username': user,
        'site_url': site_url,
        'site_name': site_name,
        'token_url': token_url
    }
    if extra_email_context is not None:
        context.update(extra_email_context)

    '''
    Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
     '''
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [user.email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)
