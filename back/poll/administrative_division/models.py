from django.db import models

from generic.models import Auditable


class Currency(Auditable):
    name = models.CharField(max_length=120, verbose_name="nombre")
    abbreviation = models.CharField(
        max_length=120, null=True, blank=True, verbose_name="abreviatura"
    )
    symbol = models.CharField(max_length=120, verbose_name="símbolo")
    is_active = models.BooleanField(default=True, verbose_name="está activo?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Divisa"
        verbose_name_plural = "Divisas"
        ordering = ["-id"]


class Country(Auditable):
    name = models.CharField(max_length=120, unique=True, verbose_name="nombre")
    phone_prefix = models.CharField(max_length=10, unique=True, verbose_name="lada")
    iso_code_alpha2 = models.CharField(
        max_length=2,
        unique=True,
        blank=True,
        null=True,
        verbose_name="código de dos letras",
    )
    iso_code_alpha3 = models.CharField(
        max_length=3,
        unique=True,
        blank=True,
        null=True,
        verbose_name="código de tres letras",
    )
    currency = models.ForeignKey(
        Currency,
        related_name="countries",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="divisa",
    )
    image = models.ImageField(blank=True, null=True, verbose_name="imagen")
    is_active = models.BooleanField(default=True, verbose_name="está activo?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ["-id"]
