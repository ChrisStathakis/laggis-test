# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-04 04:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20170503_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-updated'], 'verbose_name_plural': 'Blog'},
        ),
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name_plural': 'Κατηγορία blog'},
        ),
        migrations.AlterModelOptions(
            name='posttags',
            options={'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 4, 7, 49, 15, 11000), verbose_name='Ημερομηνία Event/Παρουσίασης'),
        ),
    ]