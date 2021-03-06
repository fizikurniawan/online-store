# Generated by Django 3.1.6 on 2021-02-06 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210206_0659'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='flashsale',
            options={'verbose_name': 'FlashSale', 'verbose_name_plural': 'FlashSales'},
        ),
        migrations.AlterModelOptions(
            name='productflashsale',
            options={'verbose_name': 'ProductFlashSale', 'verbose_name_plural': 'ProductFlashSales'},
        ),
        migrations.AddField(
            model_name='productflashsale',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
            preserve_default=False,
        ),
    ]
