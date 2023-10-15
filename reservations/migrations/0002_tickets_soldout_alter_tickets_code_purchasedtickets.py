# Generated by Django 4.2.6 on 2023-10-15 00:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='soldout',
            field=models.BooleanField(default=False, verbose_name='Sold Out'),
        ),
        migrations.AlterField(
            model_name='tickets',
            name='code',
            field=models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="Tickets' code"),
        ),
        migrations.CreateModel(
            name='PurchasedTickets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="Purchase's ID")),
                ('guestName', models.CharField(max_length=100, verbose_name="Guest's Name")),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='reservations.tickets', verbose_name='Ticket')),
            ],
            options={
                'verbose_name': 'Purchased ticket',
                'verbose_name_plural': 'Purchased tickets',
            },
        ),
    ]
