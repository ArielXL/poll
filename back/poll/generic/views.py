from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from generic import filters
from generic.models import EventLog, Config
from generic.serializers import EventLogSerializer, ConfigSerializer
from generic.tasks import doc_model_view


@doc_model_view("Generic", "event log", "event logs")
class EventLogViewSet(viewsets.ModelViewSet):
    serializer_class = EventLogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = [
        "id",
        "event_type",
        "user__name",
        "user__email",
        "user__last_name",
        "content_type__model",
    ]
    filterset_class = filters.EventLogFilter

    def get_queryset(self):
        content_types = [
            # user
            "user",
            # administrative_division
            "country",
        ]
        return EventLog.objects.filter(content_type__model__in=content_types)


class ConfigDocumentsView(APIView):
    """
    GENERIC
    -------
        Config model. \n
    GET
    ---
        Return documents. \n
    """

    serializer_class = ConfigSerializer

    def get(self, request):
        config = Config.load()
        config_serial = ConfigSerializer(config)
        return Response(config_serial.data)
