from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token


#
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True, source="user")
    password = serializers.CharField(max_length=128, write_only=True, style={"input_type": "password"})

    class Meta:
        fields = ("username", "password")

    @staticmethod
    def validate_username(value):
        try:
            user = User.objects.get(username__iexact=value)
        except User.DoesNotExist:
            message = f"User with username '{value}' does not exists."
            raise serializers.ValidationError(message)
        return user

    @staticmethod
    def check_user_password(user, password):
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Incorrect Password."})

    def validate(self, attrs):
            user = attrs.pop("user")
            password = attrs.pop("password")

            self.check_user_password(user, password)

            return {
                "token": Token.objects.get(user=user).key,
            }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

