from django.db import models

from generic.models import Auditable


class Poll(Auditable):
    question = models.CharField(max_length=255, verbose_name="pregunta")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Encuesta"
        verbose_name_plural = "Encuestas"
        ordering = ["-id"]


class Choice(Auditable):
    poll = models.ForeignKey(
        Poll,
        related_name="choices",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="encuesta",
    )
    text = models.CharField(max_length=255, verbose_name="texto")

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Elección"
        verbose_name_plural = "Elecciones"
        ordering = ["-id"]


class Vote(Auditable):
    choice = models.ForeignKey(
        Choice,
        related_name="votes",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="voto",
    )
    user_identifier = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="usuario"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["choice", "user_identifier"], name="unique_vote_per_choice_user"
            )
        ]
        verbose_name = "Voto"
        verbose_name_plural = "Votos"
        ordering = ["-id"]

    def __str__(self):
        return f"Voté for {self.choice.text} en {self.choice.poll.question}"
