# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0013_auto_20160115_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='conscious',
            field=models.IntegerField(default=-1, blank=True),
        ),
    ]
