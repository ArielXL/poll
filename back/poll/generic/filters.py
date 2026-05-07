from django_filters import DateTimeFilter
from django_filters import rest_framework as filters

from generic.models import EventLog


class EventLogFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="event_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="event_date", lookup_expr="lte")

    class Meta:
        model = EventLog
        fields = ["end_date", "start_date", "user"]
