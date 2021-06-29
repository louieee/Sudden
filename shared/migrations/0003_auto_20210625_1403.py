# Generated by Django 3.2.4 on 2021-06-25 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0002_alter_roomtype_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='height',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='width',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
