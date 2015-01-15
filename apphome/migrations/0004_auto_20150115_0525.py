# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apphome', '0003_auto_20141212_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='container_name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='container',
            name='tag',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
    ]
