# Generated by Django 3.1.7 on 2021-04-12 02:44

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_auto_20210329_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job_Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_listed',
            field=models.DateField(default=datetime.datetime(2021, 4, 12, 2, 44, 51, 620041, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Job_Type_Language_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.job_types')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.languages')),
            ],
        ),
    ]