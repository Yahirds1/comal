from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # La contraseña se acepta solo al escribir y nunca forma parte de la respuesta.
    password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "password", "is_active", "date_joined")
        read_only_fields = ("id", "date_joined", "is_active")
        extra_kwargs = {"is_active": {"required": False}}

    def validate(self, attrs):
        if self.instance is None and not attrs.get("password"):
            raise serializers.ValidationError({"password": "La contraseña es obligatoria al crear un usuario."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        # Si no llega password, se conserva el hash existente sin tocarlo.
        password = validated_data.pop("password", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone")
        read_only_fields = fields
