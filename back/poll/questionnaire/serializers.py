from django.db.models import Count

from rest_framework import serializers

from questionnaire import models


class ChoiceSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Choice
        fields = ["id", "text", "votes_count"]


class PollListSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = models.Poll
        fields = ["id", "question", "created_date", "choices"]


class PollCreateSerializer(serializers.ModelSerializer):
    choices = serializers.ListField(
        child=serializers.CharField(max_length=255), write_only=True
    )

    class Meta:
        model = models.Poll
        fields = ["id", "question", "choices"]

    def validate_choices(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Una encuesta debe tener mínimo 2 opciones."
            )

        cleaned_choices = [choice.strip() for choice in value]

        if any(choice == "" for choice in cleaned_choices):
            raise serializers.ValidationError("Las opciones no pueden estar vacías.")

        return cleaned_choices

    def create(self, validated_data):
        choices_data = validated_data.pop("choices")

        poll = models.Poll.objects.create(**validated_data)

        choices = [
            models.Choice(poll=poll, text=choice_text) for choice_text in choices_data
        ]

        models.Choice.objects.bulk_create(choices)

        return poll


class VoteSerializer(serializers.ModelSerializer):
    choice_id = serializers.IntegerField(write_only=True)
    user_identifier = serializers.CharField(write_only=True)

    class Meta:
        model = models.Vote
        fields = ["id", "choice_id", "user_identifier", "created_date"]
        read_only_fields = ["id", "created_date"]

    def validate_choice_id(self, value):
        if not models.Choice.objects.filter(id=value).exists():
            raise serializers.ValidationError("La opción seleccionada no existe.")
        return value

    def create(self, validated_data):
        choice_id = validated_data.pop("choice_id")
        user_identifier = validated_data.pop("user_identifier", "Sin nombre")

        choice = models.Choice.objects.get(id=choice_id)

        vote = models.Vote.objects.create(
            choice=choice,
            user_identifier=user_identifier,
        )

        return vote


class PollResultsChoiceSerializer(serializers.ModelSerializer):
    votes = serializers.IntegerField(source="votes_count", read_only=True)

    class Meta:
        model = models.Choice
        fields = ["text", "votes"]


class PollResultsSerializer(serializers.ModelSerializer):
    choices = serializers.SerializerMethodField()
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Poll
        fields = ["question", "total_votes", "choices"]

    def get_choices(self, obj):
        choices = obj.choices.annotate(votes_count=Count("votes"))
        return PollResultsChoiceSerializer(choices, many=True).data
