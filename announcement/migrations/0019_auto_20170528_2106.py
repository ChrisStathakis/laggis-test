# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-28 18:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0018_auto_20170528_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date_expire',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 28, 21, 6, 57, 592235), verbose_name='Ημερομηνία Λήξης'),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 28, 21, 6, 57, 592235), verbose_name='Ημερομηνία Έναρξης'),
        ),
    ]