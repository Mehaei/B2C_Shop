# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-29 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0008_order_orderinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]