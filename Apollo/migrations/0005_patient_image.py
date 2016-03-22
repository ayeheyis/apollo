# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0004_auto_20160112_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='image',
            field=models.ImageField(upload_to=b'attribute-photos', blank=True),
        ),
    ]
