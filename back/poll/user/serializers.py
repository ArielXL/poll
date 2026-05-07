from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from administrative_division.models import Country

from user import models

from user_permission.models import UserPermission
from user_permission.serializers import UserPermissionSerializer


class RoleSerializer(serializers.ModelSerializer):
    permissions_id = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        read_only=False,
        queryset=UserPermission.objects.all(),
        source="permissions",
    )
    permissions = UserPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)

    country_phone_id = serializers.IntegerField(required=False, write_only=True)
    country_phone = serializers.SerializerMethodField()

    country_id = serializers.IntegerField(required=False, write_only=True)
    country = serializers.SerializerMethodField()

    def get_country_phone(self, obj: models.User) -> dict | None:
        if obj.country_phone:
            image = obj.country_phone.image.url if obj.country_phone.image else None
            return {
                "id": obj.country_phone.id,
                "name": obj.country_phone.name,
                "phone_prefix": obj.country_phone.phone_prefix,
                "image": image,
            }
        return None

    def get_country(self, obj: models.User) -> dict | None:
        if obj.country:
            image = obj.country.image.url if obj.country.image else None
            return {
                "id": obj.country.id,
                "name": obj.country.name,
                "image": image,
            }
        return None

    def create(self, validated_data: dict) -> models.User:
        password = (
            validated_data.pop("new_password")
            if "new_password" in validated_data
            else None
        )
        roles_id = (
            validated_data.pop("roles_id") if "roles_id" in validated_data else None
        )

        obj = models.User.objects.create(**validated_data)

        if not (password is None) and (len(password) > 0):
            obj.set_password(password)
            obj.save()

        if roles_id:
            role = models.Role.objects.filter(id=roles_id)
            if role.exists():
                role = role.first()
                obj.roles.add(role)

        obj.save()
        return obj

    def update(self, instance: models.User, validated_data: dict) -> models.User:
        password = (
            validated_data.pop("new_password")
            if "new_password" in validated_data
            else None
        )
        roles_id = (
            validated_data.pop("roles_id") if "roles_id" in validated_data else None
        )

        obj = super(UserSerializer, self).update(instance, validated_data)

        if not (password is None) and (len(password) > 0):
            obj.set_password(password)
            obj.save()

        if roles_id:
            obj.roles.clear()
            role = models.Role.objects.filter(id=roles_id)
            if role.exists():
                role = role.first()
                obj.roles.add(role)

        obj.save()
        return obj

    class Meta:
        model = models.User
        fields = [
            "new_password",
            "id",
            "name",
            "last_name",
            "birth_date",
            "email",
            "phone_number",
            "country_phone_id",
            "country_phone",
            "photo",
            "gender",
            "country_id",
            "country",
            "is_active",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=models.User.objects.all(),
                fields=["country_phone_id", "phone_number"],
                message="Ya existe un usuario con ese número teléfonico",
            )
        ]


class UserMinimalSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    name = serializers.CharField()

    last_name = serializers.CharField()

    email = serializers.CharField()

    phone_number = serializers.CharField()

    country = serializers.SerializerMethodField()

    phone_prefix = serializers.SerializerMethodField()

    photo = serializers.SerializerMethodField()

    def get_country(self, obj: models.User) -> dict | None:
        if obj.country:
            return {"id": obj.country.id, "name": obj.country.name}
        return None

    def get_phone_prefix(self, obj: models.User) -> str | None:
        if obj.country_phone:
            return obj.country_phone.phone_prefix
        return None

    def get_photo(self, obj: models.User) -> str | None:
        if obj.photo:
            return obj.photo.url
        return None

    class Meta:
        model = models.User
        fields = [
            "id",
            "name",
            "last_name",
            "birth_date",
            "email",
            "phone_number",
            "phone_prefix",
            "photo",
            "gender",
            "country",
        ]


class AdminSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)

    roles_id = serializers.IntegerField(required=False, write_only=True)
    roles = serializers.SerializerMethodField()

    country_phone_id = serializers.IntegerField(required=False, write_only=True)
    country_phone = serializers.SerializerMethodField()

    country_id = serializers.IntegerField(required=False, write_only=True)
    country = serializers.SerializerMethodField()

    def get_roles(self, obj: models.User):
        role = obj.roles.filter(is_admin=True)
        if role.exists():
            role = role.first()
            return RoleSerializer(role).data
        return None

    def get_country_phone(self, obj: models.User) -> dict | None:
        if obj.country_phone:
            image = obj.country_phone.image.url if obj.country_phone.image else None
            return {
                "id": obj.country_phone.id,
                "name": obj.country_phone.name,
                "phone_prefix": obj.country_phone.phone_prefix,
                "image": image,
            }
        return None

    def get_country(self, obj: models.User) -> dict | None:
        if obj.country:
            image = obj.country.image.url if obj.country.image else None
            return {
                "id": obj.country.id,
                "name": obj.country.name,
                "image": image,
            }
        return None

    def create(self, validated_data: dict) -> models.User:
        password = (
            validated_data.pop("new_password")
            if "new_password" in validated_data
            else None
        )
        roles_id = (
            validated_data.pop("roles_id") if "roles_id" in validated_data else None
        )

        obj = models.User.objects.create(**validated_data)

        if not (password is None) and (len(password) > 0):
            obj.set_password(password)
            obj.save()

        if roles_id:
            roles = models.Role.objects.filter(id=roles_id)
            if roles.exists():
                role = roles.first()
                obj.roles.add(role)

        obj.save()
        return obj

    def update(self, instance: models.User, validated_data: dict) -> models.User:
        password = (
            validated_data.pop("new_password")
            if "new_password" in validated_data
            else None
        )
        roles_id = (
            validated_data.pop("roles_id") if "roles_id" in validated_data else None
        )

        obj = super(AdminSerializer, self).update(instance, validated_data)

        if not (password is None) and (len(password) > 0):
            obj.set_password(password)
            obj.save()

        if roles_id:
            obj.roles.clear()
            roles = models.Role.objects.filter(id=roles_id)
            if roles.exists():
                role = roles.first()
                obj.roles.add(role)

        obj.save()
        return obj

    class Meta:
        model = models.User
        fields = [
            "new_password",
            "id",
            "name",
            "last_name",
            "birth_date",
            "email",
            "phone_number",
            "country_phone_id",
            "country_phone",
            "photo",
            "gender",
            "roles_id",
            "roles",
            "country_id",
            "country",
            "is_active",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=models.User.objects.all(),
                fields=["country_phone_id", "phone_number"],
                message="Ya existe un usuario con ese número telefónico",
            )
        ]


class AdminProfileSerializer(serializers.ModelSerializer):
    phone_prefix = serializers.CharField(write_only=True, required=False)

    country_phone_id = serializers.IntegerField(required=False, write_only=True)
    country_phone = serializers.SerializerMethodField()

    country_id = serializers.IntegerField(required=False, write_only=True)
    country = serializers.SerializerMethodField()

    roles = RoleSerializer(read_only=True, many=True)

    def get_country_phone(self, obj: models.User) -> dict | None:
        if obj.country_phone:
            image = obj.country_phone.image.url if obj.country_phone.image else None
            return {
                "id": obj.country_phone.id,
                "name": obj.country_phone.name,
                "phone_prefix": obj.country_phone.phone_prefix,
                "image": image,
            }
        return None

    def get_country(self, obj: models.User) -> dict | None:
        if obj.country:
            image = obj.country.image.url if obj.country.image else None
            return {
                "id": obj.country.id,
                "name": obj.country.name,
                "image": image,
            }
        return None

    def update(self, instance: models.User, validated_data: dict) -> models.User:
        if "phone_prefix" in validated_data:
            phone_prefix = validated_data.pop("phone_prefix")
            countries = Country.objects.filter(phone_prefix=phone_prefix)
            if countries.exists():
                country = countries.first()
            else:
                raise serializers.ValidationError(
                    {"Error": "No hay ningún país con ese prefijo telefónico."}
                )
            validated_data["country_phone_id"] = country.id

        obj = super(AdminProfileSerializer, self).update(instance, validated_data)

        obj.save()
        return obj

    class Meta:
        model = models.User
        fields = "__all__"


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    google_id = serializers.CharField(write_only=True, required=False)
    device = serializers.CharField(write_only=True, required=False)
