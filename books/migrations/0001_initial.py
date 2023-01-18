# Generated by Django 4.1.5 on 2023-01-18 07:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genres', '0001_initial'),
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_stock', models.IntegerField(default=0, verbose_name='Quantity')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(max_length=1000, verbose_name='Description')),
                ('price', models.IntegerField(default=200, verbose_name='Price')),
                ('release_date', models.DateField(default=datetime.date.today, verbose_name='Date of release')),
                ('author', models.ManyToManyField(max_length=100, to='author.author', verbose_name='Author')),
                ('genres', models.ManyToManyField(to='genres.genre', verbose_name='genres')),
            ],
        ),
    ]
