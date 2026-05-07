from django.db import models


class RoleSlugTypes(models.TextChoices):
    GENERAL = "GEN", "General"
    MAINTENANCE = "MAI", "Mantenimiento"
    SUPPORT = "SUP", "Soporte"


class DeviceTypes(models.TextChoices):
    WEB = "WE", "Web"
    ANDROID = "AN", "Android"
    IOS = "IO", "iOS"


class Languages(models.TextChoices):
    SPANISH = "ES", "Español"
    ENGLISH = "EN", "Inglés"


class Genders(models.TextChoices):
    MALE = "MA", "Masculino"
    FEMALE = "FE", "Femenino"
    OTHER = "OT", "Otro"
    UNSPECIFIED = "UN", "Sin especificar"
