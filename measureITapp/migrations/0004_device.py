# Generated by Django 3.1.2 on 2021-07-26 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('measureITapp', '0003_alllabs_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ip_adress', models.CharField(max_length=16)),
                ('mac_adress', models.CharField(max_length=100)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('measure_type', models.CharField(max_length=100)),
                ('units', models.CharField(max_length=10)),
                ('connection_type', models.CharField(max_length=20)),
                ('lab_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='measureITapp.alllabs')),
            ],
        ),
    ]
