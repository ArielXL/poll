from fcm_django.models import FCMDevice

from django_filters import rest_framework as filters
from django_filters import DateTimeFilter, CharFilter


from user.models import Role, User


class RoleFilter(filters.FilterSet):
    class Meta:
        model = Role
        fields = [
            "is_admin",
            "is_staff",
            "required_country",
            "slug_key",
            "permissions",
        ]


class UserFilter(filters.FilterSet):
    start_date = DateTimeFilter(field_name="registration_date", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="registration_date", lookup_expr="lte")

    device = CharFilter(method="filter_device")

    def filter_device(self, queryset, name, value):
        devices = FCMDevice.objects.filter(type=value)
        users_id = []
        for device in devices:
            if device.user:
                users_id.append(device.user.id)
        return queryset.filter(id__in=users_id)

    class Meta:
        model = User
        fields = [
            "start_date",
            "end_date",
            "device",
            "country",
            "roles__is_admin",
            "roles__is_staff",
            "is_active",
        ]


class AdminFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
            "country",
            "is_active",
        ]
