# Generated by Django 2.2.5 on 2019-10-31 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_registeruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='number',
            field=models.CharField(max_length=12),
        ),
    ]
