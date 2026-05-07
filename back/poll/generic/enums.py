from django.db import models


class LogActions(models.TextChoices):
    DELETE = "DE", "Objeto de eliminación de usuario"
    CREATE = "CR", "Objeto de creación de usuario"
    MODIFY = "MD", "Objeto de modificación de usuario"
