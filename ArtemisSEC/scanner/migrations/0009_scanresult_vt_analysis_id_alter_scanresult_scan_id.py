# Generated by Django 5.1.6 on 2025-03-16 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0008_scanresult_file_properties_scanresult_scan_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanresult',
            name='vt_analysis_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='scanresult',
            name='scan_id',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
