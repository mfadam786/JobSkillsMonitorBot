# Generated by Django 3.1.7 on 2021-04-13 04:25

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20210412_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date_listed',
            field=models.DateField(default=datetime.datetime(2021, 4, 13, 4, 25, 1, 311671, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Job_Type_Pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay', models.IntegerField(default=0)),
                ('job_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.job_types')),
            ],
        ),
    ]
