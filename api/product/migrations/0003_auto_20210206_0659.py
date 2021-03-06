# Generated by Django 3.1.6 on 2021-02-06 06:59

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210205_1620'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlashSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('event_name', models.CharField(max_length=200)),
                ('start_event', models.DateTimeField()),
                ('end_event', models.DateTimeField()),
                ('is_published', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='stock_available',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ProductFlashSale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(db_index=True)),
                ('updated_at', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('stock', models.IntegerField(default=1)),
                ('flash_sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.flashsale')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
