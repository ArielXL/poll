from django.contrib import admin

from generic.admin import CustomModelAdmin

from .models import Poll, Choice, Vote

admin.site.register(Poll, CustomModelAdmin(Poll))
admin.site.register(Choice, CustomModelAdmin(Choice))
admin.site.register(Vote, CustomModelAdmin(Vote))
