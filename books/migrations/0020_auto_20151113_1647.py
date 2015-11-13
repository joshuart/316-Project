# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0019_auto_20151113_1616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='book_ISBN',
        ),
        migrations.AddField(
            model_name='book',
            name='fifth_author_first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='fifth_author_last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='first_author_first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='first_author_last_name',
            field=models.CharField(default='hello', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='fourth_author_first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='fourth_author_last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='second_author_first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='second_author_last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='third_author_first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='third_author_last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
    ]
