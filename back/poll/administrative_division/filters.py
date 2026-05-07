from django_filters import DateTimeFilter
from django_filters import rest_framework as filters

from administrative_division.models import Country, Currency


class CurrencyFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="created_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = Currency
        fields = ["start_date", "end_date", "is_active"]


class CountryFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="created_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = Country
        fields = ["start_date", "end_date", "currency", "is_active"]
