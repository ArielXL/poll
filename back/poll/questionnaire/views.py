from django.db.models import Count, Prefetch

from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action

from .models import Poll, Choice

from .serializers import (
    PollListSerializer,
    PollCreateSerializer,
    VoteSerializer,
    PollResultsSerializer,
)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all().order_by("-created_date")

    def get_queryset(self):
        return (
            Poll.objects.all()
            .prefetch_related(
                Prefetch(
                    "choices",
                    queryset=Choice.objects.annotate(votes_count=Count("votes")),
                )
            )
            .order_by("-created_date")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return PollCreateSerializer

        return PollListSerializer

    @action(detail=True, methods=["get"], url_path="results")
    def results(self, request, pk=None):
        poll = Poll.objects.annotate(total_votes=Count("choices__votes")).get(pk=pk)
        serializer = PollResultsSerializer(poll)
        return Response(serializer.data)


class VoteView(APIView):

    serializer_class = VoteSerializer

    def post(self, request):
        serializer = VoteSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Voto registrado correctamente."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
