"""
URL configuration for poll project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions

openapi_info = openapi.Info(
    title="Grupo AOV api",
    default_version="v1.0.0",
    description="Grupo AOV api public documentation",
    terms_of_service="https://www.grupoaov.com/",
    contact=openapi.Contact(email="ahr@grupoaov.com"),
    license=openapi.License(name="Grupo AOV", url="https://www.grupoaov.com/"),
)

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    path("user-permission/", include("user_permission.urls")),
    path("administrative-division/", include("administrative_division.urls")),
    path("generic/", include("generic.urls")),
    path("questionnaire/", include("questionnaire.urls")),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]
