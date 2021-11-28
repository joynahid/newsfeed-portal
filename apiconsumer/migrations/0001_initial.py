# Generated by Django 3.2.9 on 2021-11-28 12:40

from django.db import migrations, models
import django.db.models.deletion


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
                ('description', models.TextField(blank=True, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TopHeadlineModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=255, null=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('url', models.CharField(max_length=255, unique=True)),
                ('thumbnailUrl', models.CharField(max_length=255, null=True)),
                ('country', models.CharField(max_length=100)),
                ('publishedAt', models.DateTimeField()),
                ('source', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apiconsumer.sourcemodel')),
            ],
            options={
                'ordering': ['-publishedAt'],
            },
        ),
    ]
