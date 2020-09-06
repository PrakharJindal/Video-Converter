from rest_framework import serializers
from .models import List, UserProfile
from django.contrib.auth import authenticate         # for Token Authentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token    # for Token Authentication

from rest_framework import exceptions


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title', 'desc', 'img']


class ListOneSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title', 'desc', 'img']


class LoginSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        """Validate and authenticate the user"""
        print(data)
        username = data.get('username', ""),
        password = data.get("password")

        if username and password:
            user = authenticate(username=username[0], password=password)
            if user:
                data["user"] = user

            else:
                msg = "Unable to login with given pass"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, data):
        """Validate and authenticate the user"""
        username = data.get('username', ""),
        password = data.get("password")

        if username and password:
            User.objects.create_user(
                username[0], email=None, password=password)
            user = authenticate(username=username[0], password=password)
            if user:
                data["user"] = user

            else:
                msg = "Unable to login with given credentials"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ( 'age', 'location')

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """ 
        user = Token.objects.get(key=validated_data.get('token')).user
        student, created = UserProfile.objects.update_or_create(user=user,
        age=validated_data.pop('age') , location=validated_data.pop('location'))
        return student


class ProfileSerializer2(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('user', 'age', 'location')
