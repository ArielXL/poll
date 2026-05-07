from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import PollViewSet, VoteView

router = DefaultRouter()
router.register(r"polls", PollViewSet, basename="polls")

urlpatterns = [
    path("", include(router.urls)),
    path("vote/", VoteView.as_view(), name="vote"),
]
