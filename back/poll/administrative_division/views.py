from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from administrative_division import models, serializers
from administrative_division.filters import CountryFilter, CurrencyFilter

from generic.tasks import doc_model_view


@doc_model_view("Administrative Division", "currency", "currencies")
class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "symbol",
        "abbreviation",
    ]
    filterset_class = CurrencyFilter


@doc_model_view("Administrative Division", "country", "countries")
class CountryViewSet(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "phone_prefix",
        "iso_code_alpha2",
        "iso_code_alpha3",
    ]
    filterset_class = CountryFilter
