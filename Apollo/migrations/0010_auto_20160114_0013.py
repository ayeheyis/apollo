# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0009_statistics'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Statistics',
            new_name='Statistic',
        ),
    ]
