# Generated by Django 4.2.5 on 2023-11-18 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='item',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='items',
            field=models.ManyToManyField(related_name='wishlists', to='item.item'),
        ),
    ]
