# Generated by Django 3.2.23 on 2024-02-09 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GolfApp', '0004_auto_20240205_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='average_score',
            field=models.IntegerField(default=0),
        ),
    ]
