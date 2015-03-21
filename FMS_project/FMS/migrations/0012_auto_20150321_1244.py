# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0011_auto_20150321_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default=b'profile_images/avatar.jpg', upload_to=b'profile_images', blank=True),
        ),
    ]
