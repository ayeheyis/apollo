# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='height',
            field=models.IntegerField(blank=True),
        ),
    ]
