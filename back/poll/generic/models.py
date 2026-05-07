from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from solo.models import SingletonModel

from generic.enums import LogActions
from generic.tasks import current_request


class Config(SingletonModel):
    # host url
    host_url = models.CharField(
        max_length=120,
        default="https://django-template.com.mx/",
        verbose_name="ruta del host",
    )

    # push url
    push_url = models.CharField(
        max_length=120,
        default="https://push-template.com/push",
        verbose_name="ruta del push",
    )

    # register url
    register_url = models.CharField(
        max_length=120,
        default="https://register-template.com/register",
        verbose_name="ruta del registro",
    )

    # events url
    event_url = models.CharField(
        max_length=120,
        default="https://event-template.com.mx/event",
        verbose_name="ruta del evento",
    )

    # documents
    faq = models.FileField(
        upload_to="pdf",
        null=True,
        blank=True,
        verbose_name="fichero de preguntas más frecuentes",
    )
    terms_conditions = models.FileField(
        upload_to="pdf",
        null=True,
        blank=True,
        verbose_name="fichero de términos y condiciones",
    )
    privacy_policy = models.FileField(
        upload_to="pdf",
        null=True,
        blank=True,
        verbose_name="fichero de la política de privacidad",
    )

    def __str__(self):
        return "Configuraciones generales"

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Config, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"


class Auditable(models.Model):
    created_date = models.DateTimeField(
        auto_now_add=True,
        null=True,
        editable=False,
        blank=True,
        verbose_name="fecha y hora de creación",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
        editable=False,
        blank=True,
        null=True,
        verbose_name="usuario del responsable de la creación",
    )
    last_modified_date = models.DateTimeField(
        auto_now=True,
        null=True,
        editable=False,
        blank=True,
        verbose_name="fecha y hora de la última modificación",
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_modified",
        on_delete=models.SET_NULL,
        editable=False,
        blank=True,
        null=True,
        verbose_name="usuario del responsable de la ultima modificación",
    )

    def save(self, *args, **kwargs):
        request = current_request()
        event_type = "modify_object"
        from user.models import User

        if not self.id:
            event_type = "create_object"
            if (
                hasattr(request, "user")
                and not request.user.is_anonymous
                and isinstance(request.user, (User))
            ):
                self.created_by = request.user
        if (
            hasattr(request, "user")
            and not request.user.is_anonymous
            and isinstance(request.user, (User))
        ):
            self.last_modified_by = request.user
        super(Auditable, self).save(*args, **kwargs)
        if (
            hasattr(request, "user")
            and not request.user.is_anonymous
            and isinstance(request.user, (User))
        ):
            EventLog.objects.create(
                user=self.last_modified_by,
                content_object=self,
                event_type=event_type,
                object_id=self.id,
            )

    def delete(self, *args, **kwargs):
        request = current_request()
        from user.models import User

        if (
            hasattr(request, "user")
            and not request.user.is_anonymous
            and isinstance(request.user, (User))
        ):
            EventLog.objects.create(
                user=request.user,
                content_object=self,
                event_type="delete_object",
                object_id=self.id,
            )
        super(Auditable, self).delete(*args, **kwargs)

    class Meta:
        abstract = True


class EventLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="logs",
        on_delete=models.PROTECT,
        verbose_name="usuario",
    )
    content_type = models.ForeignKey(
        ContentType,
        related_name="content_type_logs",
        on_delete=models.PROTECT,
        verbose_name="tipo de contenido",
    )
    object_id = models.PositiveIntegerField(verbose_name="identificador del objeto")
    content_object = GenericForeignKey("content_type", "object_id")
    event_type = models.CharField(
        max_length=512, choices=LogActions.choices, verbose_name="tipo de evento"
    )
    event_date = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha y hora del evento"
    )

    class Meta:
        ordering = ["-event_date"]
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"


class ApplicationLog(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name="fecha y hora")
    log = models.TextField(blank=True, null=True, verbose_name="evento")
    request = models.JSONField(blank=True, null=True, verbose_name="solicitud")
    response = models.JSONField(blank=True, null=True, verbose_name="respuesta")
    code = models.CharField(max_length=64, blank=True, null=True, verbose_name="código")

    class Meta:
        verbose_name = "Aplicación de evento"
        verbose_name_plural = "Aplicación de eventos"
        ordering = ["-date"]
