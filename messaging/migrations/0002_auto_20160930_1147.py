# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-30 11:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messaging', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('-created_at',)},
        ),
    ]
