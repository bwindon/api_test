# Generated by Django 4.1.2 on 2022-11-08 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strava', '0006_alter_activityobject_activity_logged_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityobject',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]