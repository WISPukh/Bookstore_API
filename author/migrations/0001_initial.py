# Generated by Django 4.1.5 on 2023-01-13 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, verbose_name='First name')),
                ('second_name', models.CharField(max_length=20, verbose_name='Second name')),
            ],
        ),
    ]
