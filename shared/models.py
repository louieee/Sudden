import os

from django import template
from django.db import models
# Create your models here.
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your models here.
from utilities.python_utils import send_email


class RoomType(models.Model):
    name = models.CharField(max_length=100, default='')
    height = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    width = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    class HtmlTemplate:
        forgot_password, verify_email, welcome = range(3)
        choices = (
            (forgot_password, 'forgot_password.html'),
            (verify_email, 'verify_email.html'),
            (welcome, 'welcome.html')
        )

    name = models.CharField(max_length=50, default='')
    html = models.SmallIntegerField(choices=HtmlTemplate.choices, default=None, null=True)
    html_body = models.TextField(default='', blank=True)
    template_context = models.JSONField()
    required_context = ('subject', 'sender_email', 'sender_name', 'recipients', 'attachments')
    context = {}

    def __str__(self):
        return self.name

    def get_rendered_template(self, tpl):
        return self.get_template(tpl).render(self.get_template_context())

    def get_template_context(self):
        req_temp_context = self.template_context
        return {i: self.context[i] for i in self.context if i in req_temp_context}

    @staticmethod
    def get_template(tpl):
        return template.Template(tpl)

    def get_html_file(self):
        return f'EmailTemplates/{self.get_html_display()}'

    def get_html_body(self):
        if self.html is None:
            return self.get_rendered_template(self.html_body)
        return render_to_string(self.get_html_file(), self.get_template_context())

    def get_plain_body(self):
        return strip_tags(self.get_html_body())

    def context_complete(self, ):
        required = self.template_context + list(self.required_context)
        check_context = [x for x in required if x not in self.context]
        return check_context

    def get_recipients(self):
        return self.context.get('to', [])

    def get_attachments(self):
        attachments = self.context.get('attachments', [])
        return [at for at in attachments if os.path.exists(at)]

    def send(self):
        req = self.context_complete()
        if req.__len__() == 0:
            from_ = f"{self.context['sender_name']}<{self.context['sender_email']}>"
            html_body = self.get_html_body()
            send_email(from_, self.context['subject'], self.context['recipients'], html_body,
                       bcc=self.context.get('bcc', None), cc=self.context.get('cc', None),
                       attachments=self.context.get('attachments', None))
        else:
            raise Exception(f"Missing context fields are: {', '.join(req)} ")


