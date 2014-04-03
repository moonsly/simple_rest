# -*- coding: utf-8 -*-
from rest_framework import serializers
from simple_rest.rest.models import CustomUser


class UserListSerializer(serializers.Serializer):
    
    def to_native(self, obj):
        return obj.id


class UserSerializer(serializers.HyperlinkedModelSerializer):
    age = serializers.Field(source='calculate_age')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'age', 'gender')
