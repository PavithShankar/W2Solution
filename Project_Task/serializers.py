from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Skill, User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=250, min_length=3, write_only=True)
    firstname = serializers.CharField(max_length=200, min_length=2)
    lastname = serializers.CharField(max_length=200, min_length=2)
    email = serializers.CharField(max_length=200, min_length=2)

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'password')

    def create(self, validated_data):

        user = User.objects.create_user(
            firstname=validated_data["firstname"], lastname=validated_data["lastname"], email=validated_data["email"], password=validated_data['password'])

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=200, min_length=5)
    password = serializers.CharField(
        max_length=200, min_length=3, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid Crediential')

        return user


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('firstname', 'lastname')


class SkillSerializer(serializers.ModelSerializer):
    employeeinfo = UserSerializer(read_only=True)

    class Meta:
        model = Skill
        fields = ('id', 'skillname', 'percentage', 'employeeinfo')
