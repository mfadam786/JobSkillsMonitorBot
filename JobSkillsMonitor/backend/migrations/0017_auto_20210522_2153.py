# Generated by Django 3.1.7 on 2021-05-22 09:53

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20210520_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date_listed',
            field=models.DateField(default=datetime.datetime(2021, 5, 22, 9, 53, 12, 47098, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Frameword_Listing_Count',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('framework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.frameworks')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.listing')),
            ],
        ),
    ]
