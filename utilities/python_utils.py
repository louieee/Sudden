from Sudden import settings
from customer.models import Client
from django.core.mail import EmailMessage


def get_schema(request, public=settings.DOMAIN):
    schema = request.META.get('HTTP_X_DTS_SCHEMA', None)
    if schema is None:
        host = request.get_host().split(public)[0][:-1]
        if Client.objects.filter(schema_name=host.replace('.', '_')).exists():
            return host
        return 'public'
    return schema


def get_schema_from_url(url, local='localhost'):
    return url.split(local)[0][:-1].replace('.', '_')


def send_email(sender, subject, to, message, bcc=None, cc=None, attachments=None, reply=False, is_html=True):
    if cc is None:
        cc = []
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=sender,
        to=to)
    if bcc:
        email.bcc = bcc
    if cc:
        email.cc = cc
    if reply:
        email.reply_to = to
    if attachments:
        [email.attach(attachment['file_name'], attachment['content'],
                      attachment['mimetype']) for attachment in attachments]
    if is_html:
        email.content_subtype = 'html'
    email.send()
