# Generated by Django 4.2.6 on 2023-10-17 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_alter_purchasedtickets_ticket'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tickets',
            old_name='maxPurchaseCount',
            new_name='max_purchase_count',
        ),
        migrations.RenameField(
            model_name='tickets',
            old_name='purchaseCount',
            new_name='purchase_count',
        ),
    ]