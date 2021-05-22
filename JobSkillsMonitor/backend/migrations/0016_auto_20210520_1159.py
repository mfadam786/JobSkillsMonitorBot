# Generated by Django 3.1.7 on 2021-05-19 23:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0015_auto_20210414_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frameworks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('framework', models.TextField(default='', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_listed',
            field=models.DateField(default=datetime.datetime(2021, 5, 19, 23, 58, 58, 705283, tzinfo=utc)),
        ),
    ]