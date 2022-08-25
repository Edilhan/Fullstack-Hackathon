from cProfile import label
from urllib import request
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):

    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password',
            'password_confirm', 'first_name', 'last_name', 'phone_number'
        ] 

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        return email

    def validate(self, attrs):
        p1 = attrs['password']
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError(
                'Passwords does not match'
            )
        return attrs

    def create(self, validated_data):
        print('CREATING USER WITH DATA:', validated_data)
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(label='Password', style={'input_type':'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                message = 'Unable to log in with provided info'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Must include "email" and "password"'
            raise serializers.ValidationError(message, code='authorization')
        
        attrs['user'] = user
        return attrs
