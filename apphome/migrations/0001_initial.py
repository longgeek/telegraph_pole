# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cid', models.CharField(max_length=80, null=True, blank=True)),
                ('size', models.CharField(max_length=40, null=True, blank=True)),
                ('flavor_id', models.CharField(max_length=20)),
                ('user_id', models.CharField(max_length=25)),
                ('name', models.CharField(max_length=80, null=True, blank=True)),
                ('command', models.CharField(max_length=200, null=True, blank=True)),
                ('created', models.CharField(max_length=40, null=True, blank=True)),
                ('status', models.CharField(max_length=40, null=True, blank=True)),
                ('ports', models.CharField(max_length=200, null=True, blank=True)),
                ('hostname', models.CharField(max_length=80, null=True, blank=True)),
                ('create_status', models.BooleanField(default=False, verbose_name='Create_Status')),
                ('json_extra', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=150)),
                ('port', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('total_cpu', models.IntegerField()),
                ('total_mem', models.IntegerField()),
                ('total_sys_disk', models.IntegerField()),
                ('total_volume', models.IntegerField()),
                ('total_bandwidth', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iid', models.CharField(max_length=80)),
                ('tag', models.CharField(max_length=40)),
                ('created', models.CharField(max_length=40)),
                ('repository', models.CharField(max_length=40)),
                ('virtual_size', models.CharField(max_length=20)),
                ('os_type', models.CharField(blank=True, max_length=25, null=True, choices=[(b'ubuntu', b'Ubuntu'), (b'centos', b'Centos')])),
                ('os_version', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='host',
            name='image',
            field=models.ManyToManyField(to='apphome.Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='container',
            name='host',
            field=models.ForeignKey(blank=True, to='apphome.Host', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='container',
            name='image',
            field=models.ForeignKey(to='apphome.Image'),
            preserve_default=True,
        ),
    ]
