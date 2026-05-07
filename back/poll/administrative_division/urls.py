from django.urls import include, path

from rest_framework.routers import DefaultRouter

from administrative_division import views

router = DefaultRouter()

router.register(r"currencies", views.CurrencyViewSet, basename="currency")
router.register(r"countries", views.CountryViewSet, basename="country")

urlpatterns = [path("", include(router.urls))]
