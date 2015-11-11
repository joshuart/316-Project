# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0010_auto_20151110_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='seller_email',
            field=models.EmailField(max_length=200),
        ),
    ]
