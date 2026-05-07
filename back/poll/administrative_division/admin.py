from django.contrib import admin

from generic.admin import CustomModelAdmin

from .models import Country, Currency

admin.site.register(Currency, CustomModelAdmin(Currency))
admin.site.register(Country, CustomModelAdmin(Country))
