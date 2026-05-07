from datetime import datetime

from fcm_django.models import FCMDevice

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from user import models, serializers, filters, tasks

from generic.tasks import doc_model_view


@doc_model_view("User", "role", "roles")
class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ["id", "name", "slug", "slug_key"]
    filterset_class = filters.RoleFilter


@doc_model_view("User", "user", "users")
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "email",
        "last_name",
        "phone_number",
    ]
    filterset_class = filters.UserFilter

    def get_queryset(self):
        return (
            models.User.objects.exclude(roles__is_admin=True)
            .exclude(roles__is_staff=True)
            .distinct()
        )


@doc_model_view("User", "admin", "admins")
class AdminViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdminSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "name",
        "email",
        "last_name",
        "phone_number",
        "fcmdevice__type",
    ]
    filterset_class = filters.AdminFilter

    def get_queryset(self):
        return models.User.objects.filter(roles__is_admin=True).distinct()


class AdminLoginView(CreateAPIView):
    """
    ## USER
    POST
    ----
        Logs in an admin user and generates an authentication token. This token is used for future requests that require authentication. \n
        The token is deleted and regenerated every time the user logs in, so multiple sessions are not allowed. \n
        The device field is used to determine the type of device the user is logging in from, and the google_id field is used to generate a
        unique token for the device using Firebase Cloud Messaging. This allows the user to receive push notifications on their device.

    """

    serializer_class = serializers.LoginSerializer
    permission_classes = [AllowAny]
    queryset = models.User.objects.filter(roles__is_admin=True)

    def create(self, request):
        serial = self.serializer_class(data=request.data)

        if serial.is_valid():
            email = serial.validated_data.get("email")
            password = serial.validated_data.get("password")
            google_id = serial.validated_data.get("google_id")
            device = serial.validated_data.get("device")

            admin = models.GeneralAdmin.get_from_credentials(
                self.get_queryset(), None, email
            )

            if admin:
                if not admin.check_password(password):
                    return Response(
                        {
                            "Error": "Contraseña o número telefónico incorrectos",
                            "code": "no_match_found",
                        },
                        status.HTTP_400_BAD_REQUEST,
                    )
                if not admin.is_active:
                    return Response(
                        {"Error": "El usuario no está activo", "code": "not_active"},
                        status.HTTP_400_BAD_REQUEST,
                    )

                Token.objects.filter(user=admin).delete()
                token = Token.objects.create(user=admin)
                FCMDevice.objects.filter(user__pk=admin.pk).delete()
                device = FCMDevice.objects.create(
                    user=admin, registration_id=google_id, type=device
                )
                admin.last_logged_device = tasks.complete_device(device.type)
                admin.last_logging_datetime = datetime.today()
                admin.save()

                return Response(
                    {
                        "token": str(token),
                        "user": serializers.UserMinimalSerializer(admin).data,
                        "code": "ok",
                    },
                    status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "Error": "Contraseña o número telefónico incorrectos",
                        "code": "no_match_found",
                    },
                    status.HTTP_400_BAD_REQUEST,
                )

        return Response(serial.errors, status.HTTP_400_BAD_REQUEST)


class AdminProfileView(RetrieveUpdateAPIView):
    """
    ## USER
    ### Admin profile model. \n
    GET
    ---
        Shows the profile of the authenticated user. \n
    PUT
    ---
        Modifies all fields of the authenticated user. \n
    PATCH
    -----
        Partially modifies the fields of the authenticated user. \n
    """

    serializer_class = serializers.AdminProfileSerializer
    queryset = models.User.objects.filter(roles__is_admin=True)
    permission_classes = [IsAuthenticated]
    search_fields = [
        "id",
        "name",
        "email",
        "last_name",
        "phone_number",
    ]

    def get_object(self):
        return self.request.user


class LogoutView(APIView):
    """
    ## USER
    POST
    ----
        Logs out a user and deletes the authentication code previously generated. This prevents multiple sessions.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        if not request.user.is_anonymous:
            Token.objects.filter(user=request.user).delete()
            FCMDevice.objects.filter(user=request.user).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
