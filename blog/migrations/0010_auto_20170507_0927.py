# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-07 06:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20170506_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='active_english',
            field=models.BooleanField(default=False, verbose_name='Εμφάνιση στην Αγγλική Version'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 7, 9, 27, 28, 590276), verbose_name='Ημερομηνία Event/Παρουσίασης'),
        ),
    ]