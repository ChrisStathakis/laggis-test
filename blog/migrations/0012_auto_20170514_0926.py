# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-14 06:26
from __future__ import unicode_literals

import blog.models
import datetime
from django.db import migrations, models
# import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20170507_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=blog.models.upload_file),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 14, 9, 26, 31, 522677), verbose_name='Ημερομηνία Event/Παρουσίασης'),
        ),
    ]