# Generated by Django 4.1.5 on 2023-01-18 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
    ]
