# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-04-18 22:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20180418_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internshiptaskanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.InternshipTaskQuestion'),
        ),
    ]
