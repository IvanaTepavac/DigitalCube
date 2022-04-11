from rest_framework import serializers

from .models import Users


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register/Sign up serializer
    """
    class Meta:
        model = Users
        fields = ('full_name', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = Users.objects.create_user(validated_data['username'],
                                         password=validated_data['password'],
                                         full_name=validated_data['full_name'],
                                         email=validated_data['email'],
                                         )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'full_name', 'email', 'username', 'password')
