from django.db import models
from django.contrib import admin

from solo.admin import SingletonModelAdmin

from generic.models import ApplicationLog, Config, EventLog


def CustomModelAdmin(model, inlines=[]):
    return type(
        "SubClass" + model.__name__,
        (admin.ModelAdmin,),
        {
            "list_display": [x.name for x in model._meta.fields],
            "list_select_related": [
                x.name
                for x in model._meta.fields
                if isinstance(
                    x,
                    (
                        models.ManyToOneRel,
                        models.ForeignKey,
                        models.OneToOneField,
                    ),
                )
            ],
            "search_fields": ["id"],
            "list_display_links": ["id"],
            "inlines": inlines,
        },
    )


class ApplicationLogAdmin(admin.ModelAdmin):
    base_model = ApplicationLog

    readonly_fields = ("date",)
    list_display = ("id", "code", "date", "request", "response")
    search_fields = ["id", "code"]
    list_display_links = ("id", "code")


admin.site.register(EventLog, CustomModelAdmin(EventLog))
admin.site.register(ApplicationLog, ApplicationLogAdmin)
admin.site.register(Config, SingletonModelAdmin)
