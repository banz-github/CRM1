# Generated by Django 4.2 on 2023-07-26 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_order_color_order_fabric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='barangay',
            field=models.CharField(default='Barangay Sample', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='municipality',
            field=models.CharField(default='Sample, City', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='province',
            field=models.CharField(default='Sample Province', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='region',
            field=models.CharField(default='Region Sample', max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='street',
            field=models.CharField(default='123# Sample Street', max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Order Rejected', 'Order Rejected'), ('Processing', 'Processing'), ('Ready for pickup', 'Ready for pickup'), ('Order Completed', 'Order Completed')], max_length=235, null=True),
        ),
    ]
