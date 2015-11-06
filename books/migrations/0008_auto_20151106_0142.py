# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0007_remove_book_seller_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bid_time', models.DateTimeField(verbose_name=b'bid time')),
                ('bid_price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('bidder_email', models.EmailField(max_length=254, verbose_name=b'auth.User')),
                ('seller_email', models.EmailField(max_length=254, verbose_name=b'auth.User')),
                ('listing_start_time', models.DateTimeField(verbose_name=b'date posted')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(verbose_name=b'date posted')),
                ('course_dept', models.CharField(max_length=8)),
                ('course_num', models.IntegerField(default=0)),
                ('professor', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('author_first_name', models.CharField(max_length=200, null=True)),
                ('author_last_name', models.CharField(max_length=200)),
                ('edition', models.IntegerField(default=1)),
                ('condition', models.CharField(default=b'good', max_length=9, choices=[(b'poor', b'Poor'), (b'fair', b'Fair'), (b'good', b'Good'), (b'excellent', b'Excellent'), (b'new', b'New')])),
                ('price', models.IntegerField(default=0.99)),
                ('is_auction', models.IntegerField()),
                ('is_buy_it_now', models.IntegerField(default=0)),
                ('description', models.TextField(max_length=500)),
                ('buy_it_now_price', models.IntegerField(default=0)),
                ('start_price', models.IntegerField(default=models.IntegerField(default=0))),
                ('current_bid', models.DecimalField(max_digits=5, decimal_places=2)),
            ],
            options={
                'db_table': 'listing',
            },
        ),
        migrations.RemoveField(
            model_name='book',
            name='condition',
        ),
        migrations.RemoveField(
            model_name='book',
            name='course_dept',
        ),
        migrations.RemoveField(
            model_name='book',
            name='course_num',
        ),
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.RemoveField(
            model_name='book',
            name='post_date',
        ),
        migrations.RemoveField(
            model_name='book',
            name='price',
        ),
        migrations.RemoveField(
            model_name='book',
            name='professor',
        ),
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, serialize=False, primary_key=True),
        ),
        migrations.AlterModelTable(
            name='book',
            table=None,
        ),
        migrations.AddField(
            model_name='listing',
            name='book_ISBN',
            field=models.ForeignKey(to='books.Book'),
        ),
        migrations.AddField(
            model_name='listing',
            name='seller_email',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='book_ISBN',
            field=models.ForeignKey(to='books.Book'),
        ),
    ]
