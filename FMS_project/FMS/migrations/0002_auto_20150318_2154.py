# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='projectAssigned',
            field=models.BooleanField(default=False),
        ),
    ]
