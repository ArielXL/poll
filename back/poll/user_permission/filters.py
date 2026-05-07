from django_filters import DateTimeFilter
from django_filters import rest_framework as filters

from user_permission.models import PermissionType, PermissionAction, UserPermission


class PermissionTypeFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="created_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = PermissionType
        fields = ["start_date", "end_date", "is_active"]


class PermissionActionFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="created_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = PermissionAction
        fields = ["start_date", "end_date", "is_active"]


class UserPermissionFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="created_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="created_date", lookup_expr="lte")

    class Meta:
        model = UserPermission
        fields = [
            "start_date",
            "end_date",
            "type",
            "actions",
            "is_active",
        ]
