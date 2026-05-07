from django import forms
from django.contrib import admin
from django.forms import ModelForm, PasswordInput

from generic.admin import CustomModelAdmin

from .models import Role, User


class UserForm(ModelForm):
    new_password = forms.CharField(widget=PasswordInput(), required=False)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if len(self.data["new_password"]) > 0:
            user.set_password(self.data["new_password"])
            user.save()
        return user

    class Meta:
        model = User
        exclude = ["password"]


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "last_name", "email", "phone_number")
    search_fields = ["id", "name", "last_name", "email", "phone_number"]
    list_display_links = ("id", "name", "last_name", "email", "phone_number")
    form = UserForm


admin.site.register(User, UserAdmin)
admin.site.register(Role, CustomModelAdmin(Role))
