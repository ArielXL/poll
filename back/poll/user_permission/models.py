from django.db import models

from generic.models import Auditable


class PermissionType(Auditable):
    name = models.TextField(
        max_length=120, null=True, blank=True, verbose_name="nombre"
    )
    slug = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name="clave identificadora",
    )
    is_active = models.BooleanField(default=True, verbose_name="está activo?")

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Tipo de permiso"
        verbose_name_plural = "Tipos de permisos"
        ordering = ["-id"]


class PermissionAction(Auditable):
    name = models.TextField(max_length=120, verbose_name="nombre de la acción")
    slug = models.CharField(
        max_length=100,
        unique=True,
        blank=False,
        verbose_name="clave identificadora",
    )
    is_active = models.BooleanField(default=True, verbose_name="está activo?")

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = "Acción del permiso"
        verbose_name_plural = "Acciones de los permisos"
        ordering = ["-id"]


class UserPermission(Auditable):
    name = models.CharField(
        max_length=120,
        null=True,
        blank=True,
        verbose_name="nombre",
    )
    description = models.CharField(
        max_length=300, verbose_name="descripción", blank=True
    )
    type = models.ForeignKey(
        PermissionType,
        related_name="user_permissions",
        null=True,
        blank=False,
        on_delete=models.PROTECT,
        verbose_name="Tipo de permiso",
    )
    actions = models.ManyToManyField(
        PermissionAction,
        related_name="user_permissions",
        blank=True,
        verbose_name="Acciones permitidas",
    )
    is_active = models.BooleanField(default=True, verbose_name="está activo?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Permiso de usuario"
        verbose_name_plural = "Permisos de usuarios"
        ordering = ["-id"]
