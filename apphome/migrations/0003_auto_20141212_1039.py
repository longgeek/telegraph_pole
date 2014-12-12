# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apphome', '0002_auto_20141212_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='ports',
            field=models.CharField(max_length=400, null=True, blank=True),
            preserve_default=True,
        ),
    ]
