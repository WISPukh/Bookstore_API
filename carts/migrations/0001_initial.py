# Generated by Django 4.1.5 on 2023-01-25 12:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CART', 'In cart'), ('AWAITING_ARRIVAL', 'Awaiting_arrival'), ('AWAITING_PAYMENT', 'Awaiting payment'), ('PAID', 'Paid'), ('AWAITING_DELIVERY', 'Awaiting delivery'), ('SENT', 'Sent'), ('FINISHED', 'Finished')], default='CART', max_length=50, verbose_name='State')),
                ('order_id', models.CharField(blank=True, max_length=250, null=True, verbose_name="Order's id")),
                ('amount', models.IntegerField(null=True, verbose_name='Quantity')),
                ('warranty_days', models.IntegerField(default=30, verbose_name='Dates of warranty')),
                ('orders_time', models.DateTimeField(blank=True, null=True, verbose_name='Orders date time field')),
                ('city', models.CharField(default='12345', max_length=100, verbose_name='Delivery city')),
                ('address', models.CharField(default='12345', max_length=250, verbose_name='Delivery address')),
                ('total_orders_price', models.IntegerField(blank=True, null=True, verbose_name='Total price of order')),
                ('book', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='books.book', verbose_name='Item')),
            ],
        ),
    ]
