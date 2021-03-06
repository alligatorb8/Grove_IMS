# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-06 06:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_auto_20170511_0817'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counselor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counselor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_counselor', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrgUnit')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counselor_view_permission', models.BooleanField(default=True)),
                ('intern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='org_intern', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrgUnit')),
            ],
        ),
        migrations.AlterField(
            model_name='internapplication',
            name='applicant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Application_Interns', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='internshipfocusendanswers',
            name='focus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='focus_answers', to='app.InternshipFocus'),
        ),
    ]
