# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0007_auto_20160113_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='alive',
            field=models.BooleanField(default=True),
        ),
    ]
