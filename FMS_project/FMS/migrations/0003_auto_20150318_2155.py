# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0002_auto_20150318_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisor',
            name='availability',
            field=models.BooleanField(default=True),
        ),
    ]
