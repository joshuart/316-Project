# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0018_auto_20151113_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='start_time',
            field=models.IntegerField(),
        ),
    ]
