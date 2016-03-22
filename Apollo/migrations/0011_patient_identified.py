# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0010_auto_20160114_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='identified',
            field=models.BooleanField(default=False),
        ),
    ]
