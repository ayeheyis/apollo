# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0014_patient_conscious'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='emergency',
            field=models.IntegerField(default=-1, blank=True),
        ),
    ]
