# Generated by Django 3.2.25 on 2024-04-24 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GolfApp', '0008_auto_20240329_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='is_etiquette_leader',
        ),
    ]
