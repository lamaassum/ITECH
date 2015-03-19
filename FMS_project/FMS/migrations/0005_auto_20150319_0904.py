# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0004_auto_20150319_0716'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='project',
            name='level',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='advisor',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='advisor_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='degree',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='major',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='job_title',
            field=models.CharField(max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(max_length=500, blank=True),
        ),
    ]
