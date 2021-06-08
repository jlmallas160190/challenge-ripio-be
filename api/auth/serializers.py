from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from app.blockchain.models import Account
from rest_framework import serializers

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True,min_length=8, max_length=64)
    password_confirmation = serializers.CharField(write_only=True,min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=50)
    last_name = serializers.CharField(min_length=2, max_length=100)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirmation',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class AccountRegisterSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer(required=True)

    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserRegisterSerializer.create(
            UserRegisterSerializer(), validated_data=user_data)
        account, created = Account.objects.update_or_create(user=user)
        return account