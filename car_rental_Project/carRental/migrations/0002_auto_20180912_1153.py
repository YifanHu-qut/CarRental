# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-09-12 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carRental', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MakeName', models.CharField(max_length=20)),
                ('Model', models.CharField(max_length=20)),
                ('Series', models.CharField(max_length=20)),
                ('SeriesYear', models.CharField(max_length=20)),
                ('PriceNew', models.CharField(max_length=20)),
                ('EngineSize', models.CharField(max_length=20)),
                ('FuelSystem', models.CharField(max_length=20)),
                ('TankPacity', models.CharField(max_length=20)),
                ('Power', models.CharField(max_length=20)),
                ('SeatingCapacity', models.CharField(max_length=20)),
                ('StandardTransmission', models.CharField(max_length=20)),
                ('BodyType', models.CharField(max_length=20)),
                ('Drive', models.CharField(max_length=20)),
                ('WheelBase', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('Customer_id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('CustomerName', models.CharField(max_length=20)),
                ('PhoneNumber', models.CharField(default='Null', max_length=20)),
                ('Address', models.CharField(max_length=100)),
                ('Birthday', models.CharField(default='Null', max_length=20)),
                ('Occupation', models.CharField(default='Null', max_length=20)),
                ('Gender', models.CharField(default='Null', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('Order_ID', models.IntegerField(max_length=20, primary_key=True, serialize=False)),
                ('Order_CreateDate', models.CharField(default='Null', max_length=20)),
                ('Order_PickupDate', models.CharField(default='Null', max_length=20)),
                ('Order_PickupStore', models.CharField(default='Null', max_length=20)),
                ('Order_ReturnDate', models.CharField(default='Null', max_length=20)),
                ('Order_ReturnStore', models.CharField(default='Null', max_length=20)),
                ('Customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carRental.Customer')),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
