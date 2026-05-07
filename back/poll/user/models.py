from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from administrative_division.models import Country

from generic.models import Auditable

from user.enums import DeviceTypes, Genders, Languages, RoleSlugTypes

from user_permission.models import UserPermission


class UserManager(BaseUserManager):
    def create_user(
        self, email, password, name, last_name, phone_number=None, country_phone=None
    ):
        if not email:
            raise ValueError("El usuario necesita un correo electrónico")

        user = self.model(email=self.normalize_email(email))

        user.set_password(password)
        user.name = name
        user.last_name = last_name

        user.phone_number = phone_number
        user.country_phone = country_phone
        user.save()
        return user

    def create_superuser(self, email, password, name, last_name):
        user = self.create_user(
            email=email, password=password, name=name, last_name=last_name
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Role(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="nombre")
    is_admin = models.BooleanField(default=False, verbose_name="es administrador?")
    is_staff = models.BooleanField(default=False, verbose_name="es staff?")
    required_country = models.BooleanField(default=False, verbose_name="requiere país?")
    slug_key = models.CharField(
        max_length=3,
        choices=RoleSlugTypes.choices,
        blank=True,
        null=True,
        default=RoleSlugTypes.GENERAL,
        verbose_name="clave",
    )
    slug = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        default="",
        unique=True,
        verbose_name="clave identificadora",
    )
    permissions = models.ManyToManyField(
        UserPermission,
        related_name="roles",
        blank=True,
        default=None,
        verbose_name="permisos",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["-id"]


class User(AbstractBaseUser, Auditable):
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="nombre")
    last_name = models.CharField(
        max_length=128, blank=True, null=True, verbose_name="apellidos"
    )
    birth_date = models.DateField(
        blank=True, null=True, verbose_name="fecha de nacimiento"
    )
    email = models.EmailField(
        max_length=128,
        unique=True,
        blank=True,
        null=True,
        verbose_name="correo electrónico",
    )
    phone_number = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="teléfono"
    )
    country_phone = models.ForeignKey(
        Country,
        related_name="country_phone_users",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="lada",
    )
    photo = models.ImageField(null=True, blank=True, verbose_name="imagen")

    preferred_language = models.CharField(
        max_length=2,
        choices=Languages.choices,
        blank=True,
        null=True,
        default=Languages.SPANISH,
        verbose_name="idioma",
    )
    registration_date = models.DateTimeField(
        blank=True, null=True, verbose_name="hora y fecha de registro"
    )

    is_active = models.BooleanField(default=False, verbose_name="está activo?")
    is_verified = models.BooleanField(default=False, verbose_name="está verificado?")
    is_blocked = models.BooleanField(default=False, verbose_name="está bloqueado?")

    last_logged_device = models.CharField(
        max_length=2,
        choices=DeviceTypes.choices,
        blank=True,
        null=True,
        verbose_name="tipo del dispositivo del último registro",
    )

    gender = models.CharField(
        max_length=2,
        choices=Genders.choices,
        default=Genders.UNSPECIFIED,
        verbose_name="sexo",
    )
    roles = models.ManyToManyField(Role, related_name="users", verbose_name="roles")

    is_staff = models.BooleanField(default=False, verbose_name="es staff?")
    is_superuser = models.BooleanField(default=False, verbose_name="es super usuario?")

    country = models.ForeignKey(
        Country,
        related_name="users",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="país",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "last_name"]

    objects = UserManager()

    def __str__(self):
        name = self.name if self.name else ""
        last_name = self.last_name if self.last_name else ""
        if self.name or self.last_name:
            return f"{name} {last_name}"
        else:
            return "No name"

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True

    def has_perm(self, perm, obj=None):
        return True

    def has_perms(self, perm, obj=None):
        return True

    @property
    def phone(self):
        phone_prefix = (
            self.country_phone.phone_prefix
            if self.country_phone and self.country_phone.phone_prefix
            else ""
        )
        phone_number = self.phone_number if self.phone_number else ""

        return f"{phone_prefix}{phone_number}"

    @property
    def full_name(self):
        name = self.name if self.name else ""
        last_name = self.last_name if self.last_name else ""

        return f"{name} {last_name}"

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
        return None

    @staticmethod
    def get_from_credentials(queryset, phone_prefix, phone_number):
        try:
            user = queryset.get(
                country_phone__phone_prefix=phone_prefix, phone_number=phone_number
            )
        except:
            try:
                user = queryset.get(email=phone_number)
            except:
                user = None
        return user

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        unique_together = (
            "country_phone",
            "phone_number",
        )
        ordering = ["-id"]


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(roles__name="Admin")


class GeneralAdmin(User):
    is_active_rol = models.BooleanField(default=False, verbose_name="tiene rol activo?")

    objects = AdminManager()

    def save(self, *args, **kwargs):
        created = True if not self.id else False

        super(GeneralAdmin, self).save(*args, **kwargs)
        if created:
            general_admin_role = Role.objects.get(name="Admin")
            if not general_admin_role in self.roles.all():
                self.roles.add(general_admin_role)
