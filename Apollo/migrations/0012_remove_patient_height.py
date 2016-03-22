# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0011_patient_identified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='height',
        ),
    ]
