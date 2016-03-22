# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Apollo', '0006_auto_20160113_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to=b'', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='tent',
            field=models.ForeignKey(blank=True, to='Apollo.Tent', null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=models.CharField(default=b'', max_length=40, blank=True),
        ),
        migrations.AddField(
            model_name='injury',
            name='patient',
            field=models.ForeignKey(to='Apollo.Patient'),
        ),
    ]
