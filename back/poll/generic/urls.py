from django.urls import include, path

from rest_framework.routers import DefaultRouter

from generic import views

router = DefaultRouter()

router.register(r"event-logs", views.EventLogViewSet, basename="event-log")

urlpatterns = [
    path("", include(router.urls)),
    path("documents/", views.ConfigDocumentsView.as_view()),
]
