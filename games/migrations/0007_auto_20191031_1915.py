# Generated by Django 2.2.5 on 2019-10-31 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_auto_20191031_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeruser',
            name='number',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
    ]
