import django_tables2 as tables
from .models import ActivityObject


class ActivityObjectTable(tables.Table):
    #start_date_local = tables.Column(accessor="start_date_local", localize=False)

    class Meta:
        model = ActivityObject
        start_date_local = tables.Column(order_by=("start_date_local"))
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "type", "start_date_local", "distance", "average_speed")
