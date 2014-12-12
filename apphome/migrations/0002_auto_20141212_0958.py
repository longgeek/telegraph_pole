# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apphome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='json_extra',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
