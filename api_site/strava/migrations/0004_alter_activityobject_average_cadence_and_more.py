# Generated by Django 4.1.2 on 2022-11-06 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava', '0003_alter_activityobject_average_cadence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityobject',
            name='average_cadence',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='activityobject',
            name='average_heartrate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='activityobject',
            name='average_speed',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='activityobject',
            name='max_heartrate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='activityobject',
            name='max_speed',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
