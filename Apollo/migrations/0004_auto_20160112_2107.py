# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0003_auto_20160112_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='height',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='priority',
            field=models.IntegerField(default=-1, blank=True),
        ),
    ]
