# Generated by Django 2.2.14 on 2020-12-02 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_home', '0008_auto_20201202_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_by_seller',
            name='discount_price_by_seller',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='item_by_seller',
            name='price_by_seller',
            field=models.FloatField(default=0, null=True),
        ),
    ]
