# Generated by Django 2.0.4 on 2018-05-04 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManagementSystem', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('year', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
