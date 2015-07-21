# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0004_auto_20150711_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendship',
            name='invite_status',
            field=models.BooleanField(default=False),
        ),
    ]
