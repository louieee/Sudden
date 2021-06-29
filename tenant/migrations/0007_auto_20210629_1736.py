# Generated by Django 3.2.4 on 2021-06-29 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant', '0006_alter_mail_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='is_html',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mail',
            name='message',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='attachments',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='mail',
            name='bcc',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='mail',
            name='cc',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AlterField(
            model_name='mail',
            name='context',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='mail',
            name='recipients',
            field=models.JSONField(default=list),
        ),
    ]