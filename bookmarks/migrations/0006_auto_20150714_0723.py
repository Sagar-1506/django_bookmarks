# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmarks', '0005_friendship_invite_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_link',
        ),
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.ForeignKey(related_name='from_set', default='1', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.ForeignKey(related_name='to_set', default='2', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
