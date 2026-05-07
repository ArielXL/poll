from rest_framework import serializers

from generic import models


class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Config
        fields = ["faq", "terms_conditions", "privacy_policy"]


class AuditableSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    last_modified_by = serializers.SerializerMethodField()

    def get_created_by(self, obj: models.Auditable):
        if obj.created_by:
            return {
                "id": obj.created_by.id,
                "name": obj.created_by.name,
                "email": obj.created_by.email,
                "last_name": obj.created_by.last_name,
            }
        return None

    def get_last_modified_by(self, obj: models.Auditable):
        if obj.last_modified_by:
            return {
                "id": obj.last_modified_by.id,
                "name": obj.last_modified_by.name,
                "email": obj.last_modified_by.email,
                "last_name": obj.last_modified_by.last_name,
            }
        return None

    class Meta:
        model = models.Auditable
        fields = "__all__"


class EventLogSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    model_name = serializers.SerializerMethodField()

    def get_model_name(self, obj: models.EventLog):
        return obj.content_type.model

    def get_user(self, obj: models.EventLog):
        return {
            "id": obj.user.id,
            "name": obj.user.name,
            "email": obj.user.email,
            "last_name": obj.user.last_name,
        }

    class Meta:
        model = models.EventLog
        exclude = ["content_type"]
