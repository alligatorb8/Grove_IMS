# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 21:44
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InternApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.TextField(blank=True, max_length=500)),
                ('notes', models.TextField(blank=True, max_length=500)),
                ('state', models.CharField(choices=[('submitted', 'Application Submitted'), ('pending', 'Application Pending Review'), ('approved', 'Application Approved'), ('denied', 'Application Denied'), ('needsclarification', 'Application Needs Clarification'), ('waitlist', 'Application Waitlisted')], default='submitted', max_length=36)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_start_date', models.DateTimeField()),
                ('registration_end_date', models.DateTimeField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(max_length=640)),
                ('openings', models.PositiveIntegerField(default=1)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('details', models.TextField(max_length=640)),
                ('estimation', models.DurationField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Internship')),
            ],
        ),
        migrations.CreateModel(
            name='InternshipTaskAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipTaskEndAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.PositiveIntegerField(default=5, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)])),
                ('intern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipTaskEndQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('question', models.TextField()),
                ('order', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipTaskProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('progress', models.DecimalField(choices=[(Decimal('0.000'), '0-25%'), (Decimal('0.250'), '25%'), (Decimal('0.375'), '25-50%'), (Decimal('0.500'), '50%'), (Decimal('0.625'), '50-75%'), (Decimal('0.750'), '75%'), (Decimal('0.875'), '70-99%'), (Decimal('1.000'), '100% Complete')], decimal_places=3, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipTaskQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.InternshipTask')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=128)),
                ('street', models.CharField(blank=True, max_length=128)),
                ('street2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=128)),
                ('state', models.CharField(blank=True, max_length=128)),
                ('zip', models.CharField(blank=True, max_length=128)),
                ('country', models.CharField(blank=True, max_length=128)),
                ('image', models.ImageField(default='/static/images/default_user.png', upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('member_type', models.CharField(choices=[('intern', 'Intern'), ('internsuper', 'Organization Supervisor'), ('orgmain', 'Organization Main Contact'), ('coundelor', 'Career / Guidance counselor'), ('grove', 'Grove Employee'), ('parentguardian', 'Parent or Legal Guardian'), ('other', 'Other')], default='Other', max_length=36)),
                ('email_validated', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrgUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=128, unique=True)),
                ('org_type', models.CharField(choices=[('enterprise', 'Enterprise'), ('nonprofit', 'Non-Profit'), ('primaryeducation', 'Primary Education / K-12'), ('secondaryeducation', 'Secondary / Higher Education'), ('other', 'Other')], default='Other', max_length=36)),
                ('street', models.CharField(blank=True, max_length=128)),
                ('street2', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=128)),
                ('state', models.CharField(blank=True, max_length=128)),
                ('zip', models.CharField(blank=True, max_length=128)),
                ('country', models.CharField(blank=True, max_length=128)),
                ('industry', models.CharField(default='Unknown', max_length=128)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('logo', models.ImageField(default='/static/images/default_company.png', upload_to='')),
                ('website', models.URLField(blank=True, default=None)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('intern_limit', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='internshiptaskprogress',
            name='intern',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='internshiptaskprogress',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.InternshipTask'),
        ),
        migrations.AddField(
            model_name='internshiptaskendanswers',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.InternshipTaskEndQuestion'),
        ),
        migrations.AddField(
            model_name='internshiptaskendanswers',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.InternshipTask'),
        ),
        migrations.AddField(
            model_name='internshiptaskanswer',
            name='intern',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Member'),
        ),
        migrations.AddField(
            model_name='internshiptaskanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.InternshipTaskQuestion'),
        ),
        migrations.AddField(
            model_name='internship',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.OrgUnit'),
        ),
        migrations.AddField(
            model_name='internship',
            name='main_contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='internapplication',
            name='internship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Internship'),
        ),
    ]
