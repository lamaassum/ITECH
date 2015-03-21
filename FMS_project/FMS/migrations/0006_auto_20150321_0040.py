# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0005_auto_20150319_0904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='project_choices',
            field=models.ManyToManyField(to=b'FMS.Project', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='supervisor_choices',
            field=models.ManyToManyField(to=b'FMS.Supervisor', null=True, blank=True),
        ),
    ]
