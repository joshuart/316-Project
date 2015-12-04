# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0025_auto_20151204_1403'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='fifth_author_first_name',
            new_name='fifth_author_name',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='first_author_last_name',
            new_name='first_author_name',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='fifth_author_last_name',
            new_name='fourth_author_name',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='first_author_first_name',
            new_name='second_author_name',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='fourth_author_first_name',
            new_name='third_author_name',
        ),
        migrations.RemoveField(
            model_name='book',
            name='fourth_author_last_name',
        ),
        migrations.RemoveField(
            model_name='book',
            name='second_author_first_name',
        ),
        migrations.RemoveField(
            model_name='book',
            name='second_author_last_name',
        ),
        migrations.RemoveField(
            model_name='book',
            name='third_author_first_name',
        ),
        migrations.RemoveField(
            model_name='book',
            name='third_author_last_name',
        ),
    ]
