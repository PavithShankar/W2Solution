from decimal import Context
from functools import partial
from django.contrib.auth.models import Permission
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import generics, permissions
from .models import Skill, User
from .permissions import IsEmployee
from .serializers import RegisterSerializer, SkillSerializer, UserSerializer, LoginSerializer, UpdateSerializer
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView


class RegisterApiview(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.save()

        return Response({
            "User": UserSerializer(user_data, context=self.get_serializer_context()).data,
            "Token": AuthToken.objects.create(user_data)[1]
        })


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.get_serializer(data=user)
        serializer.is_valid(raise_exception=True)

        Userdata = serializer.validated_data

        return Response({
            "user": UserSerializer(Userdata, context=self.get_serializer_context()).data,
            "Token": AuthToken.objects.create(Userdata)[1]
        })


class UpdateUserApiView(generics.UpdateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = UpdateSerializer

    def put(self, request, *args, **kwargs):
        user_data = request.data
        serializer = self.serializer_class(
            self.request.user, data=user_data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        breakpoint()
        return Response({
            'User': UserSerializer(request.user).data
        })


class GetEmployeeApiview(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()

    def get_queryset(self):

        data = User.objects.all()

        return data


class SkillListCreateApi(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Skill.objects.all()

    def perform_create(self, serializer):

        data = self.request.user
        print(data)
        skilldata = serializer.save(employeeinfo=data)

        return skilldata

    def get_queryset(self):
        return self.queryset.filter(employeeinfo=self.request.user)


class SkillGetbyidUpdateDeleteApi(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = (permissions.IsAuthenticated, IsEmployee,)
    queryset = Skill.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        breakpoint()
        return self.queryset.filter(employeeinfo=self.request.user)
