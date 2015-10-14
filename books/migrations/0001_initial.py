# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_date', models.DateTimeField(verbose_name=b'date posted')),
                ('course_dept', models.CharField(max_length=8)),
                ('course_num', models.IntegerField(default=0)),
                ('professor', models.CharField(max_length=200)),
                ('edition', models.IntegerField(default=1)),
                ('condition', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=0.99)),
                ('isbn10', models.IntegerField(default=0)),
                ('isbn13', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='seller_email',
            field=models.ForeignKey(to='books.Seller'),
        ),
    ]
