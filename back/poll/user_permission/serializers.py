from rest_framework import serializers

from user_permission import models

from generic.serializers import AuditableSerializer


class PermissionTypeSerializer(AuditableSerializer):
    class Meta:
        model = models.PermissionType
        fields = "__all__"


class PermissionActionSerializer(AuditableSerializer):
    class Meta:
        model = models.PermissionAction
        fields = "__all__"


class UserPermissionSerializer(AuditableSerializer):
    type_id = serializers.IntegerField(required=False, write_only=True)
    type = serializers.SerializerMethodField()

    actions_id = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        read_only=False,
        queryset=models.PermissionAction.objects.all(),
        source="actions",
    )
    actions = PermissionActionSerializer(many=True, read_only=True)

    def get_type(self, obj: models.UserPermission) -> dict | None:
        if obj.type:
            return {
                "id": obj.type.id,
                "slug": obj.type.slug,
                "name": obj.type.name,
            }
        return None

    class Meta:
        model = models.UserPermission
        fields = "__all__"
