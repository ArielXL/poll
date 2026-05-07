from django.urls import include, path

from rest_framework.routers import DefaultRouter

from user import views

router = DefaultRouter()

router.register(r"roles", views.RoleViewSet, basename="role")
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"admins", views.AdminViewSet, basename="admin")

urlpatterns = [
    path("admin-login/", views.AdminLoginView.as_view()),
    path("admin-profile/", views.AdminProfileView.as_view()),
    path("logout/", views.LogoutView.as_view()),
    path("", include(router.urls)),
]
