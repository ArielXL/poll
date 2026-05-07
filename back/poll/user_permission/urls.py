from django.urls import include, path

from rest_framework.routers import DefaultRouter

from user_permission import views

router = DefaultRouter()

router.register(
    r"permission-types", views.PermissionTypeViewSet, basename="permission-type"
)
router.register(
    r"permission-actions", views.PermissionActionViewSet, basename="permission-action"
)
router.register(
    r"user-permissions", views.UserPermissionViewSet, basename="user-permission"
)

urlpatterns = [path("", include(router.urls))]
