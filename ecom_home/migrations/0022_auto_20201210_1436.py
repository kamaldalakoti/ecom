# Generated by Django 2.2.14 on 2020-12-10 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_home', '0021_auto_20201209_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_cancelled',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_dispatched',
            field=models.BooleanField(default=False, null=True),
        ),
    ]