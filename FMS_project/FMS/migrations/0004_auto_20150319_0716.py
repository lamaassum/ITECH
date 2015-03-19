# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0003_auto_20150318_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default=b'', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(default=b'', max_length=500),
            preserve_default=True,
        ),
    ]
