from rest_framework import serializers

from administrative_division import models

from generic.serializers import AuditableSerializer


class CurrencySerializer(AuditableSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"


class CountrySerializer(AuditableSerializer):
    currency_id = serializers.IntegerField(required=False, write_only=True)
    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = models.Country
        fields = "__all__"
        optional_fields = ["iso_code_alpha2", "iso_code_alpha3"]
