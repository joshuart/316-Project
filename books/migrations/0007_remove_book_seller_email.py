# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20151027_1806'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='seller_email',
        ),
    ]
