# Generated by Django 3.2.9 on 2022-01-05 14:19

from django.db import migrations, models
import velox_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('velox_app', '0015_measure_dlc_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='measure',
            name='dlc_gaf_image',
            field=velox_app.models.GCSField(blank=True, null=True, verbose_name='DLC GAF Image'),
        ),
        migrations.AddField(
            model_name='measure',
            name='dlc_h5_file',
            field=velox_app.models.GCSField(blank=True, null=True, verbose_name='DLC H5 File'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='gcs_bucket',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='GCS Bucket'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='gcs_filename',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='GCS Filename'),
        ),
        migrations.AlterField(
            model_name='measure',
            name='gcs_path',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='GCS Path'),
        ),
    ]
