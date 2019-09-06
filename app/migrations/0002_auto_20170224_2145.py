# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 21:45
from __future__ import unicode_literals
from django.db import migrations


def load_stores_from_fixtures(apps, schema_editor):
    from django.core.management import call_command
    call_command("loaddata", "InternshipTaskEndQuestion")


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_stores_from_fixtures),
    ]