# Generated by Django 3.2.9 on 2021-11-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SourceModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sourceId', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TopHeadlineModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('thumbnailUrl', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=100)),
                ('publishedAt', models.TimeField()),
                ('source', models.ManyToManyField(to='apiconsumer.SourceModel')),
            ],
            options={
                'ordering': ['-publishedAt'],
            },
        ),
    ]