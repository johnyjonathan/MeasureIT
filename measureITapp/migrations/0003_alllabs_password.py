# Generated by Django 3.1.2 on 2021-07-20 20:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('measureITapp', '0002_userlabs'),
    ]

    operations = [
        migrations.AddField(
            model_name='alllabs',
            name='password',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]