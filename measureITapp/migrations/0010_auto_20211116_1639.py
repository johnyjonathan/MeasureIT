# Generated by Django 3.1.2 on 2021-11-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measureITapp', '0009_auto_20211116_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='port',
            field=models.IntegerField(default='23'),
        ),
    ]