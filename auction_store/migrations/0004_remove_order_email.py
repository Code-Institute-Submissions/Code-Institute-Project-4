# Generated by Django 3.0.3 on 2020-02-26 21:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auction_store', '0003_auto_20200218_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
    ]