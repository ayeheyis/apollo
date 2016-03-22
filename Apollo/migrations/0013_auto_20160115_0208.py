# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0012_remove_patient_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(default=-1, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='sex',
            field=models.CharField(default=b'Unknown', max_length=10, blank=True),
        ),
    ]
