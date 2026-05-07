from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from user_permission import models, serializers
from user_permission.filters import (
    PermissionTypeFilter,
    PermissionActionFilter,
    UserPermissionFilter,
)

from generic.tasks import doc_model_view


@doc_model_view("User Permission", "permission type", "permission types")
class PermissionTypeViewSet(viewsets.ModelViewSet):
    queryset = models.PermissionType.objects.all()
    serializer_class = serializers.PermissionTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "slug",
    ]
    filterset_class = PermissionTypeFilter


@doc_model_view("User Permission", "permission action", "permission actions")
class PermissionActionViewSet(viewsets.ModelViewSet):
    queryset = models.PermissionAction.objects.all()
    serializer_class = serializers.PermissionActionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "slug",
    ]
    filterset_class = PermissionActionFilter


@doc_model_view("User Permission", "user permission", "user permissions")
class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = models.UserPermission.objects.all()
    serializer_class = serializers.UserPermissionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "description",
        "type__name",
    ]
    filterset_class = UserPermissionFilter
