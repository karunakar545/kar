# Generated by Django 3.2.5 on 2021-07-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0018_auto_20210709_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportstudent',
            name='description',
            field=models.TextField(max_length=300),
        ),
    ]
