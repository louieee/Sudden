from django.db import models
import json
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket

from decouple import config
from django.db import models
from django import template
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template import Context

# Create your models here.
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags


# Create your models here.

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
    required_context = ('subject', 'sender_email', 'sender_name', 'recipients', 'attachments',)
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
        check_context = [self.context.get(x, None) for x in required if self.context.get(x, None) is None]
        return check_context.__len__() == 0

    def get_recipients(self):
        return self.context.get('to', [])

    def get_attachments(self):
        attachments = self.context.get('attachments', [])
        return [at for at in attachments if os.path.exists(at)]

    def send(self):
        try:
            sender = config('SENDER_EMAIL', default='louis')
            password = config('SENDER_PASSWORD', default='pass')
            server = smtplib.SMTP(f"{config('SERVER', default='')}: {config('PORT', default='')}")
            server.starttls()
            server.login(sender, password)
            charset = "utf-8"
            if self.context_complete():
                msg = MIMEMultipart('mixed')
                msg['Subject'] = self.context['subject']
                msg['From'] = f"{self.context['sender_name']}<{self.context['sender_email']}>"
                if self.context.get('bcc', False):
                    self.context['recipients'] = self.context['recipients'] + self.context['bcc']
                if self.context.get('cc', False):
                    self.context['recipients'] = self.context['recipients'] + self.context['cc']
                msg['To'] = ' ,'.join(self.context['recipients'])
                msg_body = MIMEMultipart('alternative')
                html_body = MIMEText(self.get_html_body().encode(charset), 'html', charset)
                text_body = MIMEText(self.get_plain_body().encode(charset), 'plain', charset)
                # Add the text and HTML parts to the child container.
                msg_body.attach(text_body)
                msg_body.attach(html_body)
                # Define the attachment part and encode it using MIMEApplication.
                msg.attach(msg_body)
                attachments = self.get_attachments()
                if attachments is not None:
                    for at in attachments:
                        att = MIMEApplication(open(at, 'rb').read())
                        att.add_header('Content-Disposition', 'attachment', filename=at)
                        msg.attach(att)
                server.sendmail(f'{sender}', [msg['to']], msg.as_string())
                server.quit()
                print('email sent successfully.')
            else:
                raise Exception(f"The context fields is not complete. "
                                f"The required fields are {', '.join(self.template_context + list(self.required_context))}")
        except (socket.gaierror, smtplib.SMTPAuthenticationError):
            print('email is offline')


