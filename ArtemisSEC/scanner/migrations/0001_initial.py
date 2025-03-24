# Generated by Django 5.1.6 on 2025-03-16 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScanResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('scan_date', models.DateTimeField(auto_now_add=True)),
                ('positives', models.IntegerField(null=True)),
                ('total', models.IntegerField(null=True)),
                ('status', models.CharField(default='pending', max_length=50)),
                ('scan_id', models.CharField(max_length=255, null=True)),
                ('permalink', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
