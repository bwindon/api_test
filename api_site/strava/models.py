from datetime import datetime
from django.utils import timezone
from django.db import models
import json
import psycopg2


# Create your models here.
class StravaToken(models.Model):
    token_time = models.DateTimeField(default=datetime.now, blank=True)
    json_string = models.JSONField()

    def __str__(self):
        return 'id = %s - token_time = %s - json_string = %s' % (self.id, self.token_time, self.json_string)


class ActivityData(models.Model):
    import_time = models.DateTimeField(default=datetime.now, blank=True)
    json_activity_blob = models.JSONField()

    def __str__(self):
        return 'ID = %s - import time = %s - blob = %s' % (self.id, self.import_time, self.json_activity_blob)


class ActivityObject(models.Model):
    name = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=8, decimal_places=2)
    moving_time = models.DurationField()
    elapsed_time = models.DurationField()
    total_elevation_gain = models.DecimalField(max_digits=6, decimal_places=2)
    type = models.CharField(max_length=15)
    start_date = models.DateTimeField()
    start_date_local = models.DateTimeField()
    average_speed = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    max_speed = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    average_cadence = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    has_heartrate = models.BooleanField(blank=True, null=True)
    average_heartrate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    max_heartrate = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    activity_logged_time = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return 'id %s----name %s----start date %s----start date local %s----logged date %s' % (self.id, self.name,
                                                                                               self.start_date,
                                                                                               self.start_date_local,
                                                                                               self.activity_logged_time)
