# Generated by Django 2.0.5 on 2018-06-02 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManagementSystem', '0003_students_batch'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'permissions': (('view_class', 'Can view class'),)},
        ),
    ]
