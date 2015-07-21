# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmarks', '0003_sharedbookmark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_friend', models.ForeignKey(related_name='friend_set', to=settings.AUTH_USER_MODEL)),
                ('to_friend', models.ForeignKey(related_name='to_friend_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('send_time', models.DateTimeField(auto_now_add=True)),
                ('message_link', models.ForeignKey(to='bookmarks.Friendship')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together=set([('from_friend', 'to_friend')]),
        ),
    ]
