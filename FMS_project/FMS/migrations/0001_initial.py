# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('level', models.CharField(max_length=128)),
                ('projectAssigned', models.BooleanField(verbose_name=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('degree', models.CharField(max_length=128)),
                ('major', models.CharField(max_length=128)),
                ('advisor', models.CharField(max_length=128)),
                ('advisor_email', models.EmailField(max_length=254)),
                ('project_choices', models.ManyToManyField(to='FMS.Project', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_title', models.CharField(max_length=128)),
                ('availability', models.BooleanField(verbose_name=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('school_ID', models.ForeignKey(to='FMS.School')),
                ('topic_choices', models.ManyToManyField(to='FMS.Topic')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='user_profile',
            field=models.OneToOneField(to='FMS.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='supervisor_choices',
            field=models.ManyToManyField(to='FMS.Supervisor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student',
            name='user_profile',
            field=models.OneToOneField(to='FMS.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='project_topic',
            field=models.ManyToManyField(to='FMS.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.ForeignKey(to='FMS.Supervisor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='project',
            field=models.ForeignKey(to='FMS.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='student',
            field=models.ForeignKey(to='FMS.Student'),
            preserve_default=True,
        ),
    ]
