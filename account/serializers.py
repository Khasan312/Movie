from django.contrib.auth import authenticate
from rest_framework import serializers

#TODO: register serializer
from account.models import MyUser
from account.utils import send_activation_code


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('passwords dont match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email, password=password)
        send_activation_code(email=user.email, activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Must include "email" and "password".'
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs



class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)
    name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(required=False)

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Адрес электронной почты уже зарегистрирован')
        return email

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, attrs):
        user = MyUser.objects.create_user(**attrs)
        send_activation_code(user.email, user.activation_code)
        return user




class ActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(min_length=8, max_length=8, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_code(self, code):
        if not MyUser.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return code

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        if not MyUser.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return attrs

    def activate(self):
        email = self.validated_data.get('email')
        user = MyUser.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField()

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate(self, attrs):
        request = self.context.get('request')
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(username=email, password=password, request=request)
            if not user:
                raise serializers.ValidationError('Введены неверные данные')
        else:
            raise serializers.ValidationError('Электронная почта и пароль обязательны')
        attrs['user'] = user
        return attrs