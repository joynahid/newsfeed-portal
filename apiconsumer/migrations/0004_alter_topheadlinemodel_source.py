# Generated by Django 3.2.9 on 2021-11-27 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apiconsumer', '0003_auto_20211127_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topheadlinemodel',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apiconsumer.sourcemodel'),
        ),
    ]
