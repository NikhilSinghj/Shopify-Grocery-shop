# Generated by Django 2.1 on 2023-09-09 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopify', '0011_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product_category',
        ),
        migrations.RemoveField(
            model_name='order',
            name='purchased',
        ),
    ]
